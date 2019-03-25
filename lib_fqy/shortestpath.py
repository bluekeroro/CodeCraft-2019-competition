# -*- coding:UTF-8 -*-
from map import Map
import road
import car


def getShortestPath(trafficMap, roads, cars):
    """
    计算全源最短路径
    """
    crossRelation = trafficMap.crossRelation
    crossList = crossRelation.keys()
    path = {}

    # 初始化
    for src in crossRelation:
        path[src] = {}
        for dst in crossRelation:
            roadId = crossRelation[src][dst] if dst in crossRelation[src] else None
            length = roads[roadId].length if roadId else 999
            path[src][dst] = {'length':length, 'path':[src,dst]} if src != dst else {'length':0, 'path':[src,dst]}

    # Floyd-Warshall算法
    for k in crossList:
        for i in crossList:
            for j in crossList:
                if path[i][j]['length'] > path[i][k]['length'] + path[k][j]['length']:
                    path[i][j]['length'] = path[i][k]['length'] + path[k][j]['length']
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
    configPath = '../CodeCraft-2019/config_10'
    trafficMap = Map(configPath)
    roads = road.generateRoadInstances(configPath)
    cars = car.generateCarInstances(configPath)

    path = getShortestPath(trafficMap, roads, cars)
    print(path['6']['32'])



