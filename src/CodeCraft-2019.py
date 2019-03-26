# -*- coding:utf-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from lib import initialData
from lib.car import generateCarInstances
from lib.road import generateRoadInstances
from lib.map import Map
from lib.shortestpath import getShortestPath
from lib.myLogger import MyLogger

def main():
    if len(sys.argv) == 5:
        MyLogger.setEnable(False)
        car_path = sys.argv[1]
        road_path = sys.argv[2]
        cross_path = sys.argv[3]
        answer_path = sys.argv[4]
    else:
        car_path = '../config/car.txt'
        road_path = '../config/road.txt'
        cross_path = '../config/cross.txt'
        answer_path = '../config/answer.txt'

    # 初始化数据
    initialData.initial(car_path, cross_path, road_path)

    # 路径txt转csv
    car_path = initialData.changeTXTpathToCSV(car_path)
    road_path = initialData.changeTXTpathToCSV(road_path)
    cross_path = initialData.changeTXTpathToCSV(cross_path)

    # 获得交通图和车辆及道路的所有实例
    trafficMap = Map(cross_path, road_path)
    cars = generateCarInstances(car_path)
    roads = generateRoadInstances(road_path)

    # 计算全源最短路径
    path = getShortestPath(trafficMap, roads, cars)

    # 遍历所有车辆载入路径并构建车辆属性条目用于排序
    carList = []
    for carId in cars:
        thisCar = cars[carId]
        src = thisCar.srcCross
        dst = thisCar.dstCross

        thisCar.route = list(map(lambda x: x[:-2], path[src][dst]['path']))

        speed = thisCar.maxSpeed
        distance = path[src][dst]['length']
        planTime = thisCar.planTime
        carList.append((thisCar.id, speed, planTime, distance))

    # 排序优先级： 速度降序 》 计划出发时间升序 》 行驶距离升序 
    # 3次排序待优化为1次排序 使用cmp_to_key()
    carList = sorted(carList, key=lambda x:(x[3]), reverse=False)
    carList = sorted(carList, key=lambda x:(x[2]), reverse=False)
    carList = sorted(carList, key=lambda x:(x[1]), reverse=True)

    # 按优先级顺序载入实际出发时间并生成输出文件
    cnt = 0
    file = open(answer_path, 'w')
    for term in carList:
        thisCar = cars[term[0]]
        thisCar.leaveTime = thisCar.planTime + int(cnt)
        cnt += 0.04 # 可调的参数 0.04
        answer = '('+','.join([thisCar.id, str(thisCar.leaveTime), ','.join(thisCar.route)])+')'
        file.write(answer+'\n')

        # MyLogger.print(thisCar.id, thisCar.leaveTime, thisCar.maxSpeed)
        # MyLogger.print(term)

if __name__ == "__main__":
    from time import time
    t = time()
    main()
    MyLogger.print('The Time Consumption:',time()-t)
    """
    ss
    """

