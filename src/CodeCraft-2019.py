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
from lib.shortestpath import getShortestPath, countTurning
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
        turning = countTurning(path, trafficMap.roadRelation, src, dst)

        speed = thisCar.maxSpeed
        distance = path[src][dst]['length']
        planTime = thisCar.planTime
        carList.append((thisCar.id, speed, planTime, turning, distance))

    # 优先级排序
    carList = sorted(carList, key=lambda x: (x[4]), reverse=False)  # 行驶距离
    carList = sorted(carList, key=lambda x: (x[2]), reverse=False)  # 计划出发时间
    carList = sorted(carList, key=lambda x: (x[3]), reverse=False)  # 转向次数
    carList = sorted(carList, key=lambda x: (x[1]), reverse=True)  # 速度

    # 按速度分批次
    s8carList = [term for term in carList if term[1] >= 8]
    s6carList = [term for term in carList if 4 < term[1] <= 6]
    s4carList = [term for term in carList if 2 < term[1] <= 4]
    s2carList = [term for term in carList if term[1] <= 2]

    # 参数矩阵
    param = [
        # turning 0     1     2    <=3
        [0.02, 0.02, 0.02, 0.3],  # speed >= 8
        [0.02, 0.02, 0.04, 0.3],  # 4 <= speed <= 6
        [0.03, 0.04, 0.04, 0.3],  # 2 <= speed <= 4
        [0.03, 0.04, 0.04, 0.3]  # speed <= 2
    ]

    cnt = 0
    for i, carList in enumerate([s8carList, s6carList, s4carList, s2carList]):
        for term in carList:
            if term[3] == 0:
                cnt += param[i][0]
            if term[3] == 1:
                cnt += param[i][1]
            if term[3] == 2:
                cnt += param[i][2]
            if term[3] >= 3:
                cnt += param[i][3]
            thisCar = cars[term[0]]
            thisCar.leaveTime = thisCar.planTime + int(cnt)

    MyLogger.print(cnt)

    # 生成输出文件
    with open(answer_path, 'w') as file:
        for carId in cars:
            thisCar = cars[carId]
            answer = '(' + ','.join([thisCar.id, str(thisCar.leaveTime), ','.join(thisCar.route)]) + ')'
            file.write(answer + '\n')


if __name__ == "__main__":
    from time import time

    t = time()
    main()
    MyLogger.print('The Time Consumption:', time() - t)


