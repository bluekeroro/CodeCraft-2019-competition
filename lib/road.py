# -*- coding:UTF-8 -*-

import pandas as pd

class Road(object):
    def __init__(self, **data):
        self.id = data['id']  # 道路的id
        self.length = data['length']  # 道路的长度
        self.limitSpeed = data['speed']  # 道路的限速
        self.laneNum = data['channel']  # 道路的车道数目
        self.srcCross = data['from']  # 道路连接的起点路口
        self.dstCross = data['to']  # 道路连接的终点路口

        self.currentLane = [[] for i in range(0, self.laneNum)]  # 各车道当前存在的车辆及其位置 {1:[['10000', 5], ['10001', 3]]}
        self.willEnter = []

    def pushCar(self, car, s1):
        """
        当前道路载入车辆
        car： 车的实例
        s1： 在上一条路走过的距离
        return: 是否载入成功
        """
        speed = min(car.maxSpeed, self.limitSpeed)
        pos = speed - s1

        # 速度不够进入这条路
        if pos <= 0:
            return False

        # 遍历所有车道寻找可以载入的位置
        for n in range(0, self.laneNum):
            thisLane = self.currentLane[n]
            stopPos = thisLane[-1][1] if thisLane else self.length+1
            if stopPos - 1 != 0:
                self.currentLane[n].append([car, min(pos, stopPos-1)])
                car.currentLocRoad = self.id
                car.currentLocLane = n
                car.currentLocPos = min(pos, stopPos-1)
                return True

        # 所有车道入口处都被堵住
        return False

    # def popCar(self, car):
    #     """
    #     当前道路载出车辆
    #     car: 车的实例
    #     """
    #     # 遍历所有车道查找该车的位置
    #     for n in range(0, self.laneNum):
    #         carIds = [c[0] for c in self.currentLane[n]]
    #         try:
    #             index = carIds.index(car.id)
    #         except:
    #             pass
    #         else:
    #             break

    #     # 注意，这里不改car类实例的当前位置，因为是先push再pop
    #     self.currentLane[n].pop(index)

    def runCars(self):
        """
        运行当前道路的车辆
        """
        for n in range(thisRoad.laneNum):
            for index, c in enumerate(thisRoad.currentLane[n]):
                thisCar = c[0]
                pos = c[1]
                speed = min(self.limitSpeed, thisCar.maxSpeed)
                # 前方无车
                if index == 0:
                    pass


def generateRoadInstances(configPath):
    roadSet = {}
    roadData = pd.read_csv(configPath)
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
    configPath = '../config/road.csv'
    roads = generateRoadInstances(configPath)
    print(roads['5010-1'].__dict__)
    print(roads['5010-2'].__dict__)
    print(roads['5010-1'].length)
