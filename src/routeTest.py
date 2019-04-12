# -*- coding:UTF-8 -*-

"""
对路线进行测试
"""

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from lib.car import generateCarInstances
from lib.road import generateRoadInstances
from lib.map import Map
from lib.shortestpath import getShortestPath
from lib.myLogger import MyLogger
from lib.scheduler import Scheduler


def __loadPathTime(trafficMap, roads):
    """
    载入所有车辆的最短路径(测试用)
    """
    path = getShortestPath(trafficMap, roads)
    for carId in cars:
        thisCar = cars[carId]
        srcCross = thisCar.srcCross
        dstCross = thisCar.dstCross
        # thisCar.route = path[srcCross][dstCross]['path']
        thisCar.leaveTime = thisCar.planTime


def __loadPresetAnswer(presetAnswer_path, trafficMap, cars):
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
            thisCar.isPreset = 1 # 为了测试方便

def computeFactor(scheduler,cars,priorityCar,endclock):
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
    Tpri = scheduler.priorityCarsEndClock - priorityCar[priorityCarIdplanTimeList[0]].planTime
    MyLogger.print('优先车辆的调度时间Tpri:', Tpri)
    Te = a * Tpri + endclock
    MyLogger.print('最终调度时间Te:', Te)

if __name__ == '__main__':
    from time import time
    t = time()

    configCrossPath = '../config/cross.txt'
    configRoadPath = '../config/road.txt'
    configCarPath = '../config/car.txt'
    presetAnswer_path = '../config/presetAnswer.txt'

    trafficMap = Map(configCrossPath, configRoadPath)
    roads = generateRoadInstances(configRoadPath)
    cars = generateCarInstances(configCarPath)

    __loadPathTime(trafficMap, roads)
    __loadPresetAnswer(presetAnswer_path, trafficMap, cars)

    # cars = dict((carId,cars[carId]) for carId in cars if cars[carId].leaveTime <= 5) # 筛选出发时间
    # cars = dict((carId,cars[carId]) for carId in cars if cars[carId].maxSpeed >= 8) # 筛选最大速度
    presetCars = dict((carId,cars[carId]) for carId in cars if cars[carId].isPreset == 1) # 筛选是否预置
    # cars = dict((carId,cars[carId]) for i,carId in enumerate(cars) if i<1000) # 筛选车的数量
    priorityCar = dict((carId, cars[carId]) for carId in cars if cars[carId].isPriority == 1)  # 筛选是否优先

    scheduler = Scheduler(trafficMap, roads, presetCars)
    scheduler.setInitClock(0)
    totalClock = scheduler.run()

    computeFactor(scheduler, cars, priorityCar, totalClock)

    print('Scheduling Clock:', totalClock)
    print('The Time Consumption:', time() - t)
    print('Car Num:', len(cars))
