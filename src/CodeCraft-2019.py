# -*- coding:utf-8 -*-
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from lib.car import generateCarInstances
from lib.road import generateRoadInstances
from lib.map import Map
from lib.myLogger import MyLogger
from lib.scheduler import Scheduler


def __groupAllCars(cars):
    """
    对非预置车辆进行分组
    """
    # 过滤预置车辆
    carList = list(filter(lambda x: (x[1].isPreset == 0), cars.items()))
    # 按速度排序
    carList = sorted(carList, key=lambda x: (x[1].maxSpeed), reverse=True)

    # 分组
    groupSize = 1000
    groups = [carList[i:i + groupSize] for i in range(0, len(carList), groupSize)]
    groups = [dict(group) for group in groups]

    return groups


def loadPresetAnswer(presetAnswer_path, trafficMap, cars):
    """
    载入预置车辆的路径和实际出发时间
    """
    with open(presetAnswer_path, 'r') as f:
        f.readline()  # 跳过第一行
        for line in f:
            line = line.replace('(', '').replace(')', '').replace(' ', '').replace('\n', '')
            line = line.split(',')
            carId = line[0]
            leaveTime = int(line[1])
            route = line[2:]
            thisCar = cars[carId]
            thisCar.route = []
            crossId = thisCar.srcCross
            for r in route:
                thisCross = trafficMap.crossRelation[crossId].items()
                for next_crossId, roadId in thisCross:
                    if r == roadId[:-2]:
                        break
                thisCar.route.append(roadId)
                crossId = next_crossId
            thisCar.leaveTime = leaveTime
            thisCar.isPreset = 1  # 方便测试


def loadUnPresetAnswer(trafficMap, roads, cars, startClock):
    """
    载入非预置车辆的路径和实际出发时间
    """
    # path = getShortestPath(trafficMap, roads)

    intervel = 600
    groups = __groupAllCars(cars)
    MyLogger.print("非预置车辆分组组数：", len(groups))
    for carGroup in groups:
        # 设置出发时间
        for carId in carGroup:
            thisCar = cars[carId]
            thisCar.leaveTime = startClock
        startClock += intervel

    # MyLogger.print('clock:', startClock)


def computeFactor(scheduler, cars, priorityCar, endclock,priorityCarsEndClock):
    carsIdSpeedList = sorted(cars.keys(), key=lambda x: cars[x].maxSpeed)
    priorityCarIdSpeedList = sorted(priorityCar.keys(), key=lambda x: cars[x].maxSpeed)

    carsIdTimeList = sorted(cars.keys(), key=lambda x: cars[x].leaveTime)
    priorityCarIdTimeList = sorted(priorityCar.keys(), key=lambda x: cars[x].leaveTime)
    priorityCarIdplanTimeList = sorted(priorityCar.keys(), key=lambda x: cars[x].planTime)

    startCrossCount = len(set(cars[carId].srcCross for carId in cars))
    endCrossCount = len(set(cars[carId].dstCross for carId in cars))

    priorityStartCrossCount = len(set(priorityCar[carId].srcCross for carId in priorityCar))
    priorityEndCrossCount = len(set(priorityCar[carId].dstCross for carId in priorityCar))

    a = len(cars) / len(priorityCar) * 0.05 \
        + cars[carsIdSpeedList[-1]].maxSpeed / cars[carsIdSpeedList[0]].maxSpeed / (
                priorityCar[priorityCarIdSpeedList[-1]].maxSpeed / priorityCar[
            priorityCarIdSpeedList[0]].maxSpeed) * 0.2375 \
        + cars[carsIdTimeList[-1]].leaveTime / cars[carsIdTimeList[0]].leaveTime / (
                priorityCar[priorityCarIdTimeList[-1]].leaveTime / priorityCar[
            priorityCarIdTimeList[0]].leaveTime) * 0.2375 \
        + startCrossCount / priorityStartCrossCount * 0.2375 \
        + endCrossCount / priorityEndCrossCount * 0.2375
    MyLogger.print('系数因子a:', a)
    Tpri = priorityCarsEndClock - priorityCar[priorityCarIdplanTimeList[0]].planTime
    MyLogger.print('优先车辆的调度时间Tpri:', Tpri)
    Te = a * Tpri + endclock
    MyLogger.print('最终调度时间Te:', Te)


def main():
    if len(sys.argv) == 6:
        MyLogger.setEnable(False)
        car_path = sys.argv[1]
        road_path = sys.argv[2]
        cross_path = sys.argv[3]
        presetAnswer_path = sys.argv[4]
        answer_path = sys.argv[5]
    else:
        car_path = '../config/car.txt'
        road_path = '../config/road.txt'
        cross_path = '../config/cross.txt'
        answer_path = '../config/answer.txt'
        presetAnswer_path = '../config/presetAnswer.txt'

    # 获得交通图和车辆及道路的所有实例
    trafficMap = Map(cross_path, road_path)
    cars = generateCarInstances(car_path)
    roads = generateRoadInstances(road_path)

    # 载入预置车辆的路径和实际出发时间
    loadPresetAnswer(presetAnswer_path, trafficMap, cars)

    presetCar = dict((carId, cars[carId]) for carId in cars if cars[carId].isPreset == 1)  # 筛选是否预置
    normalCar = dict((carId, cars[carId]) for carId in cars if cars[carId].isPreset == 0 and cars[carId].isPriority == 0)  # 筛选普通车辆
    priorityCar = dict((carId, cars[carId]) for carId in cars if cars[carId].isPriority == 1 and cars[carId].isPreset == 0)  # 筛选优先不是预置的车辆

    MyLogger.print("预置车辆的数量：", len(presetCar))
    MyLogger.print("普通车辆的数量：", len(normalCar))
    MyLogger.print("总车辆的数量：", len(cars))

    priorityCarList = [priorityCar[carId] for carId in priorityCar]
    priorityCarList = sorted(priorityCarList, key=lambda x: x.maxSpeed, reverse=True)  # 速度
    # 按速度分批次
    s16carList = [term for term in priorityCarList if term.maxSpeed == 16]
    s14carList = [term for term in priorityCarList if term.maxSpeed == 14]
    s12carList = [term for term in priorityCarList if term.maxSpeed == 12]
    s10carList = [term for term in priorityCarList if term.maxSpeed == 10]
    s8carList = [term for term in priorityCarList if term.maxSpeed == 8]
    s6carList = [term for term in priorityCarList if term.maxSpeed == 6]
    s4carList = [term for term in priorityCarList if term.maxSpeed == 4]

    for i, carList in enumerate([s16carList, s14carList, s12carList, s10carList, s8carList, s6carList, s4carList]):
        for j, term in enumerate(carList):
            term.leaveTime = term.planTime + i*len(carList)+j

    priorityCar.update(presetCar)
    scheduler = Scheduler(trafficMap, roads, priorityCar)
    scheduler.setInitClock(0)
    endclock = scheduler.run(10000) # endclock = 5127
    priorityCarsEndClock=scheduler.priorityCarsEndClock
    # 载入非预置车辆的路径和实际出发时间
    loadUnPresetAnswer(trafficMap, roads, normalCar, 1000)

    scheduler = Scheduler(trafficMap, roads, normalCar)
    scheduler.setInitClock(endclock)
    endclock = scheduler.run(10000)
    MyLogger.print("调度时间:", endclock)

    # 生成输出文件
    file = open(answer_path, 'w')
    for carId in cars:
        thisCar = cars[carId]
        # 跳过预置车辆
        if thisCar.isPreset:
            continue
        thisCar.route = list(map(lambda x: x[:-2], thisCar.route))  # roadId转换
        answer = '(' + ','.join([thisCar.id, str(thisCar.leaveTime), ','.join(thisCar.route)]) + ')\n'
        file.write(answer)

    computeFactor(scheduler, cars, priorityCar, endclock,priorityCarsEndClock)


if __name__ == "__main__":
    from time import time

    t = time()
    main()
    MyLogger.print('The Time Consumption:', time() - t)
