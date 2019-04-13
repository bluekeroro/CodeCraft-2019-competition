# -*- coding:UTF-8 -*-
from lib.map import Map
import lib.road as road
import lib.car as car
from lib.myLogger import MyLogger


def getShortestPath(trafficMap, roads):
    """
    计算全源最短路径
    如果两点没有连通的路径，则shorestPathLengthDict[crossId1][crossId2]>=9999
    """
    crossRelation = trafficMap.crossRelation
    roadRelation = trafficMap.roadRelation
    crossList = sorted(crossRelation.keys(), key=lambda x: int(x))  # 去除列表里的元素的排列的随机性
    path = {}

    # 初始化
    for src in crossRelation:
        path[src] = {}
        for dst in crossRelation:
            roadId = crossRelation[src][dst] if dst in crossRelation[src] else None
            length = roads[roadId].length if roadId else 9999
            path[src][dst] = {'length': length, 'path': [src, dst]} if src != dst else {'length': 0, 'path': [src, dst]}

    for n in range(2): # 得遍历两次保证惩罚因子的完整扩散
        # Floyd-Warshall算法
        for k in crossList:
            for i in crossList:
                for j in crossList:
                    # 引入转向惩罚因子
                    r1src = path[i][k]['path'][-2]
                    r1dst = path[i][k]['path'][-1]
                    r2src = path[k][j]['path'][0]
                    r2dst = path[k][j]['path'][1]
                    # 异常： 终点源点相同的路、 不存在的路
                    try:
                        road1Id = crossRelation[r1src][r1dst]
                        road2Id = crossRelation[r2src][r2dst]
                        direction = roadRelation[road1Id][road2Id]
                        penalty = 0 if direction == 'forward' else 100 # 60为对一次转向的惩罚系数
                    except:
                        penalty = 9999

                    if path[i][j]['length'] > path[i][k]['length'] + path[k][j]['length'] + penalty:
                        path[i][j]['length'] = path[i][k]['length'] + path[k][j]['length'] + penalty
                        path[i][j]['path'] = path[i][k]['path'] + path[k][j]['path'][1:]



    # path字段由crossId转roadId
    for src in path:
        for dst in path:
            crossPass = path[src][dst]['path']
            shortestPath = []
            for i in range(len(crossPass) - 1):
                cross1 = crossPass[i]
                cross2 = crossPass[i + 1]
                if cross1 != cross2:
                    roadId = crossRelation[cross1][cross2]
                    shortestPath.append(roadId)
            path[src][dst]['path'] = shortestPath

    return path


def countTurning(path, roadRelation, src, dst):
    """
    统计转向的次数
    """
    num_forward = 0
    num_left = 0
    num_right = 0
    for i in range(len(path[src][dst]['path']) - 1):
        curRoad = path[src][dst]['path'][i]
        nextRoad = path[src][dst]['path'][i + 1]
        direction = roadRelation[curRoad][nextRoad]
        if direction == 'forward':
            num_forward += 1
        if direction == 'left':
            num_left += 1
        if direction == 'right':
            num_right += 1
    return num_left + num_right


if __name__ == '__main__':
    configCrossPath = '../config/cross.txt'
    configRoadPath = '../config/road.txt'
    configCarPath = '../config/car.txt'

    trafficMap = Map(configCrossPath, configRoadPath)
    roads = road.generateRoadInstances(configRoadPath)
    cars = car.generateCarInstances(configCarPath)

    path = getShortestPath(trafficMap, roads)
    for carId in cars:
        src = cars[carId].srcCross
        dst = cars[carId].dstCross
        p = path[src][dst]
        MyLogger.print("getShortestPath：", carId, p)
