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
    with open(presetAnswer_path, 'r') as f:
        f.readline()  # 跳过第一行
        for line in f:
            line = line.replace('(', '').replace(')', '').replace(' ', '').replace('\n', '')
            line = line.split(',')
            carId = line[0]
            leaveTime = int(line[1])
            route = line[2:]
            thisCar = cars[carId]
            crossId = thisCar.srcCross
            for r in route:
                thisCross = trafficMap.crossRelation[crossId].items()
                for next_crossId, roadId in thisCross:
                    if r == roadId[:-2]:
                        break
                thisCar.route.append(roadId)
                crossId = next_crossId
            thisCar.leaveTime = leaveTime

    # 计算全源最短路径
    path = getShortestPath(trafficMap, roads, cars)

    # 载入非预置车辆的路径和实际出发时间
    carList = []
    for carId in cars:
        thisCar = cars[carId]
        if thisCar.isPreset:
            pass
        else:
            src = thisCar.srcCross
            dst = thisCar.dstCross
            thisCar.route = path[src][dst]['path']
            thisCar.leaveTime = thisCar.planTime

    # 生成输出文件
    file = open(answer_path, 'w')
    for carId in cars:
        thisCar = cars[carId]
        thisCar.route = list(map(lambda x: x[:-2], thisCar.route))  # roadId转换
        answer = '(' + ','.join([thisCar.id, str(thisCar.leaveTime), ','.join(thisCar.route)]) + ')\n'
        file.write(answer)


if __name__ == "__main__":
    from time import time

    t = time()
    main()
    MyLogger.print('The Time Consumption:', time() - t)
