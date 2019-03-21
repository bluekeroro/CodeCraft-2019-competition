# -*- coding:UTF-8 -*-

import pandas as pd
from queue import Queue

from lib.initialData import changeTXTpathToCSV
from lib.myLogger import MyLogger


class Road(object):
    def __init__(self, **data):
        self.id = data['id']  # 道路的id
        self.length = data['length']  # 道路的长度
        self.limitSpeed = data['speed']  # 道路的限速
        self.laneNum = data['channel']  # 道路的车道数目
        self.srcCross = data['from']  # 道路连接的起点路口
        self.dstCross = data['to']  # 道路连接的终点路口

        self.currentLane = {i: Queue(self.length) for i in range(1, self.laneNum + 1)}  # 各车道当前存在的车辆


def generateRoadInstances(roadTXTpath):
    roadSet = {}
    roadData = pd.read_csv(changeTXTpathToCSV(roadTXTpath))
    for index, row in roadData.iterrows():
        data = {
            'id': str(row['id']) + '-1',
            'length': row['length'],
            'speed': row['speed'],
            'channel': row['channel'],
            'from': str(row['from']),
            'to': str(row['to']),
        }
        roadSet[data['id']] = Road(**data)

        # 如果是双向的加多一条反向的road
        if row['isDuplex']:
            data = {
                'id': str(row['id']) + '-2',
                'length': row['length'],
                'speed': row['speed'],
                'channel': row['channel'],
                'from': str(row['to']),
                'to': str(row['from']),
            }
            roadSet[data['id']] = Road(**data)

    return roadSet


if __name__ == '__main__':
    roadTXTpath = '../CodeCraft-2019/config/road.txt'
    roads = generateRoadInstances(roadTXTpath)
    MyLogger.print(roads['5010-1'].__dict__)
    MyLogger.print(roads['5010-2'].__dict__)
    MyLogger.print(roads['5010-1'].length)
