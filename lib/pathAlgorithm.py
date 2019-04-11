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

    # """以下回退到单纯Floyd-Warshall最短路径算法"""
    # roadId = shortestpath[currCrossId][dstCrossId]['path'][0]
    # for nextCrossId in crossRelation[currCrossId]:
    #     if crossRelation[currCrossId][nextCrossId] == roadId:
    #         break
    # else:
    #     raise Exception(roadId + ':Mismatch!')
    # return roadId

    # MyLogger.print('selectRoad condition', condition)
    ret_list = []
    for roadId in condition:
        for nextCrossId in crossRelation[currCrossId]:
            if crossRelation[currCrossId][nextCrossId] == roadId \
                    and shortestpath[nextCrossId][dstCrossId]['length'] \
                    < shortestpath[currCrossId][dstCrossId]['length'] \
                    and len(condition[roadId]) > 0:
                # MyLogger.print("计算", roadId, "拥挤程度")
                time, speed = useTimeInChannel(condition[roadId])
                ret_list.append(
                    [roadId, time, shortestpath[nextCrossId][dstCrossId]['length'], speed])

    if len(ret_list) == 1:
        # MyLogger.print('只有一条路径可以计算拥堵程度')
        pass
    elif len(ret_list) == 0:
        # MyLogger.print('没有路径可以计算拥堵程度')
        ret_roadId = shortestpath[currCrossId][dstCrossId]['path'][0]
        if ret_roadId not in condition:
            ret_roadId = list(condition.keys())[0]
            for roadId in condition:  # 为了保证没有绕远路  可注释该循环以减少程序运行时间
                for nextCrossId in crossRelation[currCrossId]:
                    if crossRelation[currCrossId][nextCrossId] == roadId \
                            and shortestpath[nextCrossId][dstCrossId]['length'] \
                            < shortestpath[currCrossId][dstCrossId]['length']:
                        return roadId
        return ret_roadId
    else:
        # MyLogger.print('多条路径可以计算拥堵程度')
        pass
    # ret_list = sorted(ret_list, key=lambda x: x[2])
    # ret_list = sorted(ret_list, key=lambda x: 0.4 * x[1] + 0.6 * x[2])
    ret_list = sorted(ret_list, key=lambda x: 0.301 * x[1] * x[3] + x[2])
    # MyLogger.print('selectRoad返回:', ret_list[0][0])
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
    if channel['lane'] == []:
        return 0, 0
    firstCar = channel['lane'][0][0]
    punish = 0
    if firstCar.flag == 'W':  # 第一辆车等待时 应该有惩罚
        punish = 0  # 效果不明显  暂不使用
        # MyLogger.print("第一辆车等待时 应该有惩罚")
    preTime = 0
    speed = 9999
    for (car, loc) in channel['lane']:
        currSpeed = car.maxSpeed if car.maxSpeed < channel['limitSpeed'] else channel['limitSpeed']
        time = (channel['length'] + 1 - loc) / currSpeed + 1
        if speed >= currSpeed:
            speed = currSpeed
        if preTime <= time:
            preTime = time
    # MyLogger.print(preTime)
    return preTime * (1 + punish), speed


# def selectRoad(condition, shortestpath, crossRelation, currCrossId, dstCrossId):
#     """以下回退到单纯Floyd-Warshall最短路径算法"""
#     roadId = shortestpath[currCrossId][dstCrossId]['path'][0]
#     if roadId not in condition:
#         raise Exception(roadId + ':Mismatch!')
#     return roadId


if __name__ == '__main__':
    pass
