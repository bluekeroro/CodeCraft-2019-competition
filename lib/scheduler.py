# -*- coding:UTF-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from map import Map
import road
import car
from shortestpath import getShortestPath
from queue import Queue


class Scheduler(object):
    def __init__(self, trafficMap, roads, cars):
        self.trafficMap = trafficMap
        self.roads = roads
        self.cars = cars

        self.clock = 0 # 调度时钟
        self.startQueue = Queue() # 处于起点的车辆队列
        self.endQueue = Queue() # 处于终点的车辆队列
        self.roadSchedulOrder = [] # 道路的调度顺序

        self.endflag = len(cars) # 剩余的未完成车辆
        self.existWaitCar = True # 调度循环标志位：是否存在等待调度车辆

    def showAllCarsInfo(self):
        for carId in sorted(self.cars.keys(), key=lambda x:int(x)):
            thisCar = self.cars[carId]
            if thisCar.status == 'start':
                print(carId, '  [',thisCar.currentLocRoad,'   ',thisCar.currentLocLane,'    ', thisCar.currentLocPos,']   ',thisCar.status)
            else:
                thisRoad = self.roads[thisCar.currentLocRoad]
                print(carId, '  [',thisCar.currentLocRoad,'   ', str(thisCar.currentLocLane)+'/'+str(thisRoad.laneNum),'    ', 
                    str(thisCar.currentLocPos)+'/'+str(thisRoad.length),']   ', str(thisCar.maxSpeed)+'/'+str(thisRoad.limitSpeed),
                    '     ', thisCar.status)

    def showAllRoadsInfo(self):
        for roadId in sorted(self.roads.keys(), key=lambda x:int(x[:-2])):
            thisRoad = self.roads[roadId]
            for n in range(thisRoad.laneNum):
                print(roadId, [(c[0].id,c[1]) for c in thisRoad.currentLane[n]])
            print('')

    def showSomeRoadsInfo(self):
        for roadId in sorted(self.roads.keys(), key=lambda x:int(x[:-2])):
            thisRoad = self.roads[roadId]
            for n in range(thisRoad.laneNum):
                if not thisRoad.currentLane[n]:
                    break
                print(roadId,n, [(c[0].id,c[1]) for c in thisRoad.currentLane[n]])

    def trackCarInfo(self, carId):
        thisCar = self.cars[carId]
        thisRoad = self.roads[thisCar.currentLocRoad]
        print(carId, '  [',thisCar.currentLocRoad,'   ', str(thisCar.currentLocLane)+'/'+str(thisRoad.laneNum),'    ', 
                    str(thisCar.currentLocPos)+'/'+str(thisRoad.length),']   ', str(thisCar.maxSpeed)+'/'+str(thisRoad.limitSpeed),
                    '     ', thisCar.status)

    def __initSchedule(self):
        """
        调度初始化
        """
        self.clock = 0

        for carId in sorted(self.cars.keys(), key=lambda x:int(x)):
            self.cars[carId].status = 'start'
            self.startQueue.put(carId)

        for crossId in sorted(self.trafficMap.crossRelation.keys(), key=lambda x:int(x)):
            for roadId in sorted(self.trafficMap.crossRelation[crossId].values(), key=lambda x:int(x[:-2])):
                self.roadSchedulOrder.append(roadId)

    def __initPeriod(self):
        """
        周期初始化
        """
        self.clock += 1
        for roadId in self.roads:
            # 道路的入口列表初始化为空
            self.roads[roadId].willEnter = []
            # 道路上的所有车辆初始化为等待状态
            for n in range(self.roads[roadId].laneNum):
                for thisCar, pos in self.roads[roadId].currentLane[n]:
                    thisCar.flag = 'W' 

    def __startCars(self):
        """
        调度起点车辆
        """
        for i in range(self.startQueue.qsize()):
            carId = self.startQueue.get()
            thisCar = self.cars[carId]
            # 时钟已过出发时间
            if self.clock >= thisCar.leaveTime:
                roadId = self.cars[carId].route[0]
                thisRoad = self.roads[roadId]
                hasPush, isWait = thisRoad.pushCar(thisCar, 0)
                # 进入道路成功
                if hasPush:
                    pass
                # 因为没位置而进入道路失败
                else:
                    self.startQueue.put(carId)
            # 时钟尚未过出发时间
            else:
                self.startQueue.put(carId)

    def __runCarsInRoad(self, thisRoad):
        """
        运行每条车道上的车辆
        """
        for n in range(thisRoad.laneNum):
            for index, c in enumerate(thisRoad.currentLane[n]):
                thisCar = c[0]

                # 该车已经调度完成则跳过这辆车
                if thisCar.flag == 'T':
                    continue

                pos = c[1]
                speed = min(thisRoad.limitSpeed, thisCar.maxSpeed)
                preCar = thisRoad.currentLane[n][index-1][0] if index != 0 else None
                stopPos = preCar.currentLocPos if preCar else thisRoad.length + 1

                # 不超过前车或不出道路
                if pos + speed <= stopPos-1:
                    thisRoad.currentLane[n][index][1] = pos + speed
                    thisCar.currentLocPos = pos + speed
                    thisCar.flag = 'T'
                else:
                    # 受前车阻挡
                    if preCar:
                        if preCar.flag == 'W':
                            thisCar.flag = 'W'
                        elif preCar.flag == 'T':
                            thisRoad.currentLane[n][index][1] = stopPos - 1
                            thisCar.currentLocPos = stopPos - 1
                            thisCar.flag = 'T'
                        else:
                            raise Exception("?????")
                    # 不受前车阻挡(将出路口)
                    else:
                        nextRoadId = thisCar.getNextRoadId()
                        if nextRoadId:
                            thisCar.flag = 'W'
                            direction = self.trafficMap.roadRelation[thisCar.currentLocRoad][nextRoadId]
                            if direction == 'forward':
                                direnum = 0
                            elif direction == 'left':
                                direnum = 1
                            elif direction == 'right':
                                direnum = 2
                            self.roads[nextRoadId].willEnter.append({
                                'car': thisCar,
                                's1': thisRoad.length-pos,
                                'preRoadId': thisCar.currentLocRoad,
                                'preLane': thisCar.currentLocLane,
                                'direnum': direnum, 
                                'pos': thisCar.currentLocPos,
                                'laneNum': thisCar.currentLocLane,
                                'isPriority':thisCar.isPriority})
                        # 前方无路即已到达终点
                        else:
                            thisRoad.popCar(thisCar.id)
                            thisCar.flag = 'T'
                            thisCar.status = 'end'
                            thisCar.currentLocPos = thisRoad.length
                            self.endflag -= 1

                # 检查调度完以后该车的调度状态
                if thisCar.flag == 'W':
                    self.existWaitCar = True

    def __runCarsInEntrance(self, thisRoad):
        """
        运行道路入口处车辆
        """
        # 道路入口处待入车辆优先级排序
        thisRoad.willEnter = sorted(thisRoad.willEnter, key=lambda x: (x['laneNum']), reverse=False) # 车道编号
        thisRoad.willEnter = sorted(thisRoad.willEnter, key=lambda x: (x['pos']), reverse=True) # 相对位置
        thisRoad.willEnter = sorted(thisRoad.willEnter, key=lambda x: (x['direnum']), reverse=False) # 转向
        # thisRoad.willEnter = sorted(thisRoad.willEnter, key=lambda x: (x['isPriority']), reverse=True) # 优先级
        firstDire = thisRoad.willEnter[0]['direnum'] if thisRoad.willEnter else None
        # 只遍历第一优先级转向道路的车辆
        for item in list(filter(lambda x: x['direnum']==firstDire, thisRoad.willEnter)):
            thisCar = item['car']
            s1 = item['s1']
            preRoadId = item['preRoadId']
            preLane = item['preLane']
            preRoad = self.roads[preRoadId]
            hasPush, isWait = thisRoad.pushCar(thisCar, s1)

            # 进入道路成功
            if hasPush:
                self.cars[thisCar.id].flag = 'T'
                self.roads[preRoadId].popCar(thisCar.id)
                """
                # 前道路的前车道的车再进行一次调度 #
                """
            # 进入道路失败
            else:
                # 因受阻车为等待状态而进入失败
                if isWait:
                    pass # 等待下一个大循环
                # 因没有位置或速度不够而进入失败
                else:
                    preRoad.currentLane[preLane][0][1] = preRoad.length
                    thisCar.currentLocPos = preRoad.length
                    thisCar.flag = 'T'
        # 重置该路的入口
        thisRoad.willEnter = []

    def __runCars(self):
        """
        调度路上的车辆
        """
        self.existWaitCar = True
        loop = 0
        # 直到所有车都变成终止状态T
        while self.existWaitCar:
            loop += 1
            if loop >= 50:
                raise Exception("Circular Waiting Deadlock!")

            self.existWaitCar = False

            # 第一步：在各自道路内运行车辆
            for roadId in self.roadSchedulOrder:
                thisRoad = self.roads[roadId]
                self.__runCarsInRoad(thisRoad)

            # 第二步：尝试将各自道路的入口处的车置入车道
            for roadId in self.roadSchedulOrder:
                thisRoad = self.roads[roadId]
                self.__runCarsInEntrance(thisRoad)
        return loop
        
    def run(self, clock=0):
        """
        运行调度器
        """
        self.__initSchedule()

        preloop = [0, 0]
        while self.endflag > 0:
            self.__initPeriod()

            loop = self.__runCars()
            print('loop:',loop)

            # 一个很混的判死锁方法
            if preloop[0] == loop:
                preloop[1] += 1
            else:
                preloop[0] = loop
                preloop[1] = 0
            if preloop[1] >= 20:
                raise Exception('Deadlock,loop:'+str(preloop[0]))


            self.__startCars()

            if self.clock >= clock:
                # self.showAllCarsInfo()
                self.showSomeRoadsInfo()
                # self.showAllRoadsInfo()
                input()

            print(self.clock)
        print('Scheduling Clock:', self.clock)


def __loadPathTime(trafficMap, roads, cars):
    """
    载入所有车辆的最短路径(测试用)
    """
    path = getShortestPath(trafficMap, roads, cars)
    for carId in cars:
        thisCar = cars[carId]
        srcCross = thisCar.srcCross
        dstCross = thisCar.dstCross
        thisCar.route = path[srcCross][dstCross]['path']
        thisCar.leaveTime = thisCar.planTime 


if __name__ == '__main__':
    from time import time
    t = time()

    configCrossPath = '../config/cross.txt'
    configRoadPath = '../config/road.txt'
    configCarPath = '../config/car.txt'

    trafficMap = Map(configCrossPath, configRoadPath)
    roads = road.generateRoadInstances(configRoadPath)
    cars = car.generateCarInstances(configCarPath)

    __loadPathTime(trafficMap, roads, cars)

    cars = dict((carId,cars[carId]) for carId in cars if cars[carId].leaveTime <= 1)
    cars = dict((carId,cars[carId]) for i,carId in enumerate(cars) if i<1000)

    scheduler = Scheduler(trafficMap, roads, cars)
    scheduler.run(500)

    print('The Time Consumption:', time() - t)
