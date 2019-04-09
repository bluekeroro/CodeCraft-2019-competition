# -*- coding:UTF-8 -*-


def selectRoad(condition, shortestpath, crossRelation, currCrossId, srcCrossId):
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

    srcCrossId: 终点路口id
    
    return： 返回挑选的路的id

    """

    """以下回退到单纯Floyd-Warshall最短路径算法"""
    roadId = shortestpath[currCrossId][srcCrossId]['path'][0]
    for nextCrossId in crossRelation[currCrossId]:
        if crossRelation[currCrossId][nextCrossId] == roadId:
            break
    else:
        raise Exception(roadId + ':Mismatch!')
    return roadId
    
