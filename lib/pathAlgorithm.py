# -*- coding:UTF-8 -*-
import math

from lib.myLogger import MyLogger


def selectRoad(condition, shortestpath, crossRelation, currCrossId, dstCrossId):
    """
    计算拥堵程度，选择最好的路
    condition: 待选路的路况，形如：
    {
        '10001-1'： {
            'limitSpeed': 15, 
            'length': 30, 
            'lane': [[<CarObject>, 12], [<CarObject>, 10], [<CarObject>, 4]]
        }，
        '10005-1'： {
            'limitSpeed': 10, 
            'length': 20, 
            'lane': [[<CarObject>, 8], [<CarObject>, 7], [<CarObject>, 4]]
        }
    }

    shortestpath： 最短路径，来自shortestpath.getShortestPath，形如：
    {
        crossId1:{
            crossId2:{
                'length': 120,
                'path': [6028-2', '5829-1', '5933-2']
            },
            ...
        },
        ...
    }

    crossRelation: 来自trafficMap.crossRelation，形如：
    {
        crossId1:{
            crossId2: roadId,
            ...
        },
        ...
    }

    currCrossId: 当前路口id

    dstCrossId: 终点路口id
    
    return： 返回挑选的路的id

    """

    """以下回退到单纯Floyd-Warshall最短路径算法"""
    # roadId = shortestpath[currCrossId][srcCrossId]['path'][0]
    # for nextCrossId in crossRelation[currCrossId]:
    #     if crossRelation[currCrossId][nextCrossId] == roadId:
    #         break
    # else:
    #     raise Exception(roadId + ':Mismatch!')
    MyLogger.print('selectRoad condition', condition)
    ret_list = []
    for roadId in condition:
        for nextCrossId in crossRelation[currCrossId]:
            if crossRelation[currCrossId][nextCrossId] == roadId \
                    and shortestpath[nextCrossId][dstCrossId]['length'] \
                    < shortestpath[currCrossId][dstCrossId]['length'] \
                    and len(condition[roadId]) > 0:
                MyLogger.print("计算", roadId, "拥挤程度")
                time = useTimeInChannel(condition[roadId])
                ret_list.append([roadId, time])

    if len(ret_list) == 1:
        MyLogger.print('只有一条路径可以计算拥堵程度')
    elif len(ret_list) == 0:
        MyLogger.print('没有路径可以计算拥堵程度')
        # raise RuntimeError("没有路径可以计算拥堵程度")
        return shortestpath[currCrossId][dstCrossId]['path'][0]
    else:
        MyLogger.print('多条路径可以计算拥堵程度')
    ret_list = sorted(ret_list, key=lambda x: x[1])
    MyLogger.print('selectRoad返回:', ret_list[0][0])
    return ret_list[0][0]


def useTimeInChannel(channel):
    """
    计算carObj通过该channel的时间，主要在selectRoad中调用
    :param channel:形如
    {
            'limitSpeed': 15,
            'length': 30,
            'lane': [[<CarObject>, 12], [<CarObject>, 10], [<CarObject>, 4]]
        }
    :return: (int) time
    """
    if len(channel['lane']) == 0:
        return 0
    lane = sorted(channel['lane'], key=lambda x: x[1], reverse=True)
    preTime = 0
    for (car, loc) in lane:
        currSpeed = car.maxSpeed if car.maxSpeed < channel['limitSpeed'] else channel['limitSpeed']
        time = math.ceil(float(channel['length'] + 1 - loc) / float(currSpeed))
        if preTime <= time:
            preTime = time

    return int(preTime)


if __name__ == '__main__':
    # channel = {
    #     'limitSpeed': 15,
    #     'length': 30,
    #     'lane': [[1, 12], [2, 8], [3, 2]]
    # }
    # useTimeInChannel(channel)
    pass
