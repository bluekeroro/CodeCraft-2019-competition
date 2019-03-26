# -*- coding:UTF-8 -*-
from lib.map import Map
import lib.road as road
import lib.car as car
from lib.myLogger import MyLogger


def getShortestPath(trafficMap, roads, cars):
    """
    计算全源最短路径
    """
    crossRelation = trafficMap.crossRelation
    roadRelation = trafficMap.roadRelation
    crossList = crossRelation.keys()
    path = {}

    # 初始化
    for src in crossRelation:
        path[src] = {}
        for dst in crossRelation:
            roadId = crossRelation[src][dst] if dst in crossRelation[src] else None
            length = roads[roadId].length if roadId else 9999
            path[src][dst] = {'length':length, 'path':[src,dst]} if src != dst else {'length':0, 'path':[src,dst]}

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
                    penalty = 0 if direction == 'forward' else 60 # 60为对一次转向的惩罚系数
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
            for i in range(len(crossPass)-1):
                cross1 = crossPass[i]
                cross2 = crossPass[i+1]
                if cross1 != cross2:
                    roadId = crossRelation[cross1][cross2] 
                    shortestPath.append(roadId)
            path[src][dst]['path'] = shortestPath

    return path



if __name__ == '__main__':
    configCrossPath = '../config/cross.csv'
    configRoadPath = '../config/road.csv'
    configCarPath = '../config/car.csv'

    trafficMap = Map(configCrossPath, configRoadPath)
    roads = road.generateRoadInstances(configRoadPath)
    cars = car.generateCarInstances(configCarPath)

    path = getShortestPath(trafficMap, roads, cars)
    for carId in cars:
        src = cars[carId].srcCross
        dst = cars[carId].dstCross
        p = path[src][dst]

    MyLogger.print(p)



