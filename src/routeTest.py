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


def statistics(path, cars, roadRelation):
    num_direction = 0
    num_forward = 0
    num_left = 0
    num_right = 0
    turning_times = {i:0 for i in range(10)}
    
    for carId in sorted(cars.keys()):
        src = cars[carId].srcCross
        dst = cars[carId].dstCross
        num_turning = 0

        print(carId, '', end='')
        for i in range(len(path[src][dst]['path'])-1):
            curRoad = path[src][dst]['path'][i]
            nextRoad = path[src][dst]['path'][i+1]
            direction = roadRelation[curRoad][nextRoad]
            num_direction += 1
            if direction == 'forward':
                num_forward += 1
            if direction == 'left':
                num_left += 1
                num_turning += 1
            if direction == 'right':
                num_right += 1 
                num_turning += 1
            turning_times[num_turning] += 1          

            print(direction,'- ',end='')
        print(num_turning)


    print("\n","ALL","Forward","Left","Right")
    print(num_direction,num_forward,num_left,num_right)
    print(turning_times)





if __name__ == '__main__':
    configCrossPath = '../config/cross.csv'
    configRoadPath = '../config/road.csv'
    configCarPath = '../config/car.csv'

    trafficMap = Map(configCrossPath, configRoadPath)
    roads = generateRoadInstances(configRoadPath)
    cars = generateCarInstances(configCarPath)
    roadRelation = trafficMap.roadRelation
    path = getShortestPath(trafficMap, roads, cars)

    statistics(path, cars, roadRelation)
