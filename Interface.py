# -*- coding:UTF-8 -*-
"""
@File    : Interface.py
@Time    : 2019/4/8 21:24
@Author  : Blue Keroro
"""


def selectRoad(roadDict, shorestPathLengthDict, crossRelation,crossId):
    """
    车辆在路口时，该方法判断下一条路
    :param roadDict: 形如
    {
        roadId:{    # 当前路口相邻的roadId
            channel:{  # 只提供车辆能进入的车道就可以
                length: val,    # 当前channel长度
                limitSpeed: val,    # 限速
                carObject, # carObject中需要具有在channel中的位置参数，实际速度
                ...
            }
        },
        ...
     }
    :param shorestPathLengthDict: 以便计算下个路口到终点的实际最短距离，形如
    {
        crossId1:{
            crossId2:{
                length: val,
            },
            ...
        },
        ...
    }
    :param crossRelation: fqy生成的trafficMap.crossRelation 以便知道下个路口的crossId，获取下个路口到终点的实际最短路径
    :param crossId: 当前所在路口的crossId
    :return:(str)roadId
    """
    pass


def useTimeInChannel(channel,carObj):
    """
    计算carObj通过该channel的时间，主要在selectRoad中调用
    :param channel:形如
    {
        length: val,    # 当前channel长度
        limitSpeed: val,    # 限速
        carObject, # carObject中需要具有在channel中的位置参数，实际速度
        ...
    }
    :param carObj:即将要进入车道的车辆
    :return: (int) time
    """
    pass


def getShortestPathLength(trafficMap, roads):
    """
    基于之前的弗洛伊德算法略加修改即可，不需要特别提供什么参数
    如果两点没有想通的路径，则shorestPathLengthDict[crossId1][crossId2]=None
    :param trafficMap:
    :param roads:
    :return: 返回shorestPathLengthDict
    """
    pass
