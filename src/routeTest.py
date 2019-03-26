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
from lib.shortestpath import getShortestPath, countTurning



if __name__ == '__main__':
    configCrossPath = '../config/cross.csv'
    configRoadPath = '../config/road.csv'
    configCarPath = '../config/car.csv'

    trafficMap = Map(configCrossPath, configRoadPath)
    roads = generateRoadInstances(configRoadPath)
    cars = generateCarInstances(configCarPath)
    roadRelation = trafficMap.roadRelation
    path = getShortestPath(trafficMap, roads, cars)


    turning_times = {i:0 for i in range(10)}
    for carId in cars:
        src = cars[carId].srcCross
        dst = cars[carId].dstCross
        t = countTurning(path,roadRelation,src,dst)
        turning_times[t] += 1
        
    print(turning_times)



