# -*- coding:UTF-8 -*-

import pandas as pd


class Car(object):
    def __init__(self, **data):
        self.id = data['id'] # 车的id
        self.srcCross = data['from'] # 起点路口的id
        self.dstCross = data['to'] # 终点路口的id
        self.maxSpeed = data['speed'] # 最高速度
        self.planTime = data['planTime'] # 计划出发事件

        self.route = [] # 路线
        self.leaveTime = None # 实际出发时间
        self.currentLocRoad = None # 当前所在的道路
        self.currentLocLane = None # 当前所在的车道
        self.currentLocPos = None # 当前所在距离
        
        self.status = None # 当前状态 可选 'start' | 'run' | 'end'
        self.flag = None # 当前调度状态。可选： 'W' | 'T'

def generateCarInstances(configPath):
    """
    生成所有车辆的实例
    """
    carSet = {}
    carData = pd.read_csv(configPath)
    for index, row in carData.iterrows():
        data = {
            'id': str(row['id']),
            'from': str(row['from']),
            'to': str(row['to']),
            'speed': row['speed'],
            'planTime': row['planTime'],
        }
        carSet[data['id']] = Car(**data)

    return carSet


if __name__ == '__main__':
    configPath = '../config/car.csv'
    cars = generateCarInstances(configPath)
    print(cars['10000'].__dict__)

