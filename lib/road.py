# -*- coding:UTF-8 -*-


from lib.myLogger import MyLogger


class Road(object):
    def __init__(self, **data):
        self.id = data['id']  # 道路的id
        self.length = data['length']  # 道路的长度
        self.limitSpeed = data['speed']  # 道路的限速
        self.laneNum = data['channel']  # 道路的车道数目
        self.srcCross = data['from']  # 道路连接的起点路口
        self.dstCross = data['to']  # 道路连接的终点路口

        self.currentLane = [[] for i in range(0, self.laneNum)]  # 各车道当前存在的车辆及其位置
        self.willEnter = [] # 当前周期将进入的车辆 (实例，转向，车道，位置)

    def calcRoadCondition(self):
        """
        检查当前道路可进入的车道的路况
        """
        condition = {}
        for n in range(0, self.laneNum):
            thisLane = self.currentLane[n]
            lastCar = thisLane[-1][0] if thisLane else None
            stopPos = lastCar.currentLocPos if lastCar else self.length+1
            # 受阻位不在第一位,代表将选择这条车道
            if stopPos != 1:
                condition['length'] = self.length
                condition['limitSpeed'] = self.limitSpeed
                condition['lane'] = self.currentLane[n]
                return condition
        # 所有车道的受阻位都在第一位即已经没有空位可进入
        return {}
                

    def pushCar(self, car, s1):
        """
        当前道路载入车辆
        car： 车的实例
        s1： 在上一条路走过的距离
        return: 是否载入成功, 是否需要等待下一个循环
        """
        speed = min(car.maxSpeed, self.limitSpeed)
        pos = speed - s1

        # 速度不够进入这条路
        if pos <= 0:
            return False, False

        # 遍历所有车道寻找可以载入的位置
        for n in range(0, self.laneNum):
            thisLane = self.currentLane[n]
            lastCar = thisLane[-1][0] if thisLane else None
            stopPos = lastCar.currentLocPos if lastCar else self.length+1
            # 受阻位不在第一位
            if stopPos != 1:
                # 最后一辆车存在且受阻且为等待状态
                if lastCar and pos>=stopPos and lastCar.flag == 'W':
                    # 受阻前车为等待状态,得等待下一个循环
                    return False, True
                self.currentLane[n].append([car, min(pos, stopPos-1)])
                car.currentLocRoad = self.id
                car.currentLocLane = n
                car.currentLocPos = min(pos, stopPos-1)
                car.status = 'run'
                car.flag = 'T'
                return True, False

        # 所有车道入口处都被堵住
        return False, False

    def popCar(self, carId):
        """
        当前道路载出车辆
        car: 车的实例
        """
        # 遍历所有车道查找该车的位置
        for n in range(0, self.laneNum):
            if self.currentLane[n] and self.currentLane[n][0][0].id == carId:
                break
        else:
            # for n in range(0, self.laneNum):
            #     for x in self.currentLane[n]:
            #         print(x[0].id,end=',')
            #     print('')
            raise Exception("Pop Car Fail:"+carId)
        self.currentLane[n].pop(0)

    def pushCarInwillEnter(self, item):
        """
        当前道路载入车辆到willEnter
        """
        for carItem in self.willEnter:
            if carItem['car'].id == item['car'].id:
                break
        else:
            self.willEnter.append(item)
            return True
        return False


def generateRoadInstances(configPath):
    roadSet = {}
    with open(configPath, 'r') as f:
        f.readline() # 跳过第一行
        for line in f:
            line = line.replace('(', '').replace(')', '').replace('\n', '')
            line = line.split(', ')
            data = {
                'id': line[0] + '-1',
                'length': int(line[1]),
                'speed': int(line[2]),
                'channel': int(line[3]),
                'from': line[4],
                'to': line[5],
            }
            roadSet[data['id']] = Road(**data)
            # 如果是双向的加多一条反向的road
            if int(line[6]):
                data = {
                    'id': line[0] + '-2',
                    'length': int(line[1]),
                    'speed': int(line[2]),
                    'channel': int(line[3]),
                    'from': line[5],
                    'to': line[4],
                }
                roadSet[data['id']] = Road(**data)
    return roadSet



if __name__ == '__main__':
    configPath = '../config/road.txt'
    roads = generateRoadInstances(configPath)
    MyLogger.print(roads['5000-1'].__dict__)
    MyLogger.print(len(roads))


