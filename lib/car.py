# -*- coding:UTF-8 -*-

from lib.myLogger import MyLogger


class Car(object):
    def __init__(self, **data):
        self.id = data['id'] # 车的id
        self.srcCross = data['from'] # 起点路口的id
        self.dstCross = data['to'] # 终点路口的id
        self.maxSpeed = data['speed'] # 最高速度
        self.planTime = data['planTime'] # 计划出发事件
        self.isPriority = data['isPriority'] # 是否为优先车辆
        self.isPreset = data['isPreset'] # 是否为预置车辆

        self.route = [] # 路线
        self.leaveTime = None # 实际出发时间
        self.currentLocRoad = None # 当前所在的道路
        self.currentLocLane = None # 当前所在的车道
        self.currentLocPos = None # 当前所在距离
        
        self.status = None # 当前状态 可选 'start' | 'run' | 'end'
        self.flag = None # 当前调度状态。可选： 'W' | 'T'


def generateCarInstances(configPath):
    carSet = {}
    with open(configPath, 'r') as f:
        f.readline() # 跳过第一行
        for line in f:
            line = line.replace('(', '').replace(')', '').replace('\n', '')
            line = line.split(', ')
            data = {
                'id': line[0],
                'from': line[1],
                'to': line[2],
                'speed': int(line[3]),
                'planTime': int(line[4]),
                'isPriority': int(line[5]),
                'isPreset': int(line[6]),
            }
            carSet[data['id']] = Car(**data)
    return carSet



if __name__ == '__main__':
    configPath = '../config/car.txt'
    cars = generateCarInstances(configPath)
    MyLogger.print(cars['37819'].__dict__)
