# -*- coding:utf-8 -*-
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from lib.car import generateCarInstances
from lib.road import generateRoadInstances
from lib.map import Map
from lib.shortestpath import getShortestPath, countTurning
from lib.myLogger import MyLogger
from lib.scheduler import Scheduler

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


def loadUnPresetAnswer(trafficMap, roads, cars, path):
    """
    载入非预置车辆的路径和实际出发时间
    """
    # 过滤预置车辆
    carList = list(filter(lambda x:(x[1].isPreset == 0), cars.items()))

    # 载入路径
    for carId,thisCar in carList:
        thisCar.route = path[thisCar.srcCross][thisCar.dstCross]['path']
        thisCar.turnNum = countTurning(path, trafficMap.roadRelation, thisCar.srcCross, thisCar.dstCross)

    # # 排序
    # carList = sorted(carList, key=lambda x:(x[1].shortestDistance), reverse=False) # 距离
    carList = sorted(carList, key=lambda x:(x[1].turnNum), reverse=False) # 转向
    carList = sorted(carList, key=lambda x:(x[1].maxSpeed), reverse=True) # 速度
    carList = sorted(carList, key=lambda x:(x[1].isPriority), reverse=True) # 优先

    param = [0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
    cnt = 337
    for carId,thisCar in carList:
        speed = thisCar.maxSpeed
        if speed == 4:
            cnt += param[0]
        if speed == 6:
            cnt += param[1]
        if speed == 8:
            cnt += param[2]
        if speed == 10:
            cnt += param[3]
        if speed == 12:
            cnt += param[4]
        if speed == 14:
            cnt += param[5]
        if speed == 16:
            cnt += param[6]

        thisCar.leaveTime = int(cnt)
        thisCar.route = path[thisCar.srcCross][thisCar.dstCross]['path']

    MyLogger.print(cnt)

        

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
    roads = generateRoadInstances(road_path)
    path = getShortestPath(trafficMap, roads)
    cars = generateCarInstances(car_path, path)

    # 载入预置车辆的路径和实际出发时间
    loadPresetAnswer(presetAnswer_path, trafficMap, cars)

    # 载入非预置车辆的路径和实际出发时间
    loadUnPresetAnswer(trafficMap, roads, cars, path)

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


if __name__ == "__main__":
    from time import time

    t = time()
    main()
    MyLogger.print('The Time Consumption:', time() - t)
