# -*- coding:UTF-8 -*-

from lib.car import generateCarInstances
from lib.road import generateRoadInstances
from lib.map import Map
from lib.shortestpath import getShortestPath
from lib.myLogger import MyLogger
from queue import Queue
import lib.pathAlgorithm


class Scheduler(object):
    def __init__(self, trafficMap, roads, cars):
        self.trafficMap = trafficMap
        self.roads = roads
        self.cars = cars

        self.shortestpath = getShortestPath(trafficMap, roads)

        self.clock = 0  # 调度时钟
        self.startNormalList = list()  # 处于起点的普通车辆队列
        self.startPriorityList = list()  # 处于起点的优先车辆队列
        self.endQueue = Queue()  # 处于终点的车辆队列
        self.roadSchedulOrder = []  # 道路的调度顺序

        self.endflag = len(cars)  # 剩余的未完成车辆
        self.existWaitCar = True  # 调度循环标志位：是否存在等待调度车辆

    def setInitClock(self, initClock):
        """
        设置初始时钟
        """
        self.clock = initClock

    def pickGoodRoad(self, currCrossId, dstCrossId, srcRoad='fangqy'):
        """
        在路口处选择最好的路
        """
        # 计算路口相连的路拥堵状况
        condition = {}
        crossRelation = self.trafficMap.crossRelation
        for nextCrossId in crossRelation[currCrossId]:
            roadId = crossRelation[currCrossId][nextCrossId]
            if srcRoad[:-2] != roadId[:-2]:
                thisRoad = self.roads[roadId]
                condition[roadId] = thisRoad.calcRoadCondition()

        # 计算最好的路
        goodRoadId = lib.pathAlgorithm.selectRoad(condition, self.shortestpath, crossRelation, currCrossId, dstCrossId)
        return goodRoadId

    def showAllCarsInfo(self):
        for carId in sorted(self.cars.keys(), key=lambda x: int(x)):
            thisCar = self.cars[carId]
            if thisCar.status == 'start':
                MyLogger.print(carId, '  [', thisCar.currentLocRoad, '   ', thisCar.currentLocLane, '    ',
                               thisCar.currentLocPos, ']   ', thisCar.status)
            else:
                thisRoad = self.roads[thisCar.currentLocRoad]
                MyLogger.print(carId, '  [', thisCar.currentLocRoad, '   ',
                               str(thisCar.currentLocLane) + '/' + str(thisRoad.laneNum), '    ',
                               str(thisCar.currentLocPos) + '/' + str(thisRoad.length), ']   ',
                               str(thisCar.maxSpeed) + '/' + str(thisRoad.limitSpeed),
                               '     ', thisCar.status)

    def showAllRoadsInfo(self):
        for roadId in sorted(self.roads.keys(), key=lambda x: int(x[:-2])):
            thisRoad = self.roads[roadId]
            for n in range(thisRoad.laneNum):
                MyLogger.print(roadId, [(c[0].id, c[1]) for c in thisRoad.currentLane[n]])
            MyLogger.print('')

    def showSomeRoadsInfo(self):
        for roadId in sorted(self.roads.keys(), key=lambda x: int(x[:-2])):
            thisRoad = self.roads[roadId]
            for n in range(thisRoad.laneNum):
                if not thisRoad.currentLane[n]:
                    break
                MyLogger.print(roadId, n, [(c[0].id, c[1]) for c in thisRoad.currentLane[n]])

    def trackCarInfo(self, carId):
        thisCar = self.cars[carId]
        thisRoad = self.roads[thisCar.currentLocRoad]
        MyLogger.print(carId, '  [', thisCar.currentLocRoad, '   ',
                       str(thisCar.currentLocLane) + '/' + str(thisRoad.laneNum), '    ',
                       str(thisCar.currentLocPos) + '/' + str(thisRoad.length), ']   ',
                       str(thisCar.maxSpeed) + '/' + str(thisRoad.limitSpeed),
                       '     ', thisCar.status)

    def __initSchedule(self):
        """
        调度初始化
        """
        seq = sorted(self.cars.keys(), key=lambda x: int(x))
        seq = sorted(seq, key=lambda x: self.cars[x].leaveTime)
        for carId in seq:
            self.cars[carId].status = 'start'
            if self.cars[carId].isPriority:
                self.startPriorityList.append(carId)
            else:
                self.startNormalList.append(carId)

        for crossId in sorted(self.trafficMap.crossRelation.keys(), key=lambda x: int(x)):
            for roadId in sorted(self.trafficMap.crossRelation[crossId].values(), key=lambda x: int(x[:-2])):
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
        调度起点普通车辆
        """
        i = 0
        while i < len(self.startNormalList):
            carId = self.startNormalList[i]
            thisCar = self.cars[carId]
            # 时钟已过出发时间
            if self.clock >= thisCar.leaveTime:
                # 如果不是预置车辆，在取第一条路之前先计算路况后再把第一条路push进route
                if thisCar.isPreset:
                    pass
                else:
                    goodRoadId = self.pickGoodRoad(thisCar.srcCross, thisCar.dstCross)
                    if thisCar.route == []:
                        thisCar.route.append(goodRoadId)

                roadId = self.cars[carId].route[0]
                thisRoad = self.roads[roadId]
                hasPush, isWait = thisRoad.pushCar(thisCar, 0)
                # 进入道路成功
                if hasPush:
                    self.startNormalList.pop(i)
                # 因为没位置而进入道路失败
                else:
                    i += 1
            # 时钟尚未过出发时间
            else:
                # self.startNormalQueue.put(carId)
                break

    def __startPriority(self):
        """
        调度起点优先车辆
        """
        i = 0
        while i < len(self.startPriorityList):
            carId = self.startPriorityList[i]
            thisCar = self.cars[carId]
            # 时钟已过出发时间
            if self.clock >= thisCar.leaveTime:
                # 如果不是预置车辆，在取第一条路之前先计算路况后再把第一条路push进route
                if thisCar.isPreset:
                    pass
                else:
                    goodRoadId = self.pickGoodRoad(thisCar.srcCross, thisCar.dstCross)
                    if thisCar.route == []:
                        thisCar.route.append(goodRoadId)

                roadId = self.cars[carId].route[0]
                thisRoad = self.roads[roadId]
                hasPush, isWait = thisRoad.pushCar(thisCar, 0)
                # 进入道路成功
                if hasPush:
                    self.startPriorityList.pop(i)
                # 因为没位置而进入道路失败
                else:
                    i += 1
            # 时钟尚未过出发时间
            else:
                break


    def __runCarsInLane(self, thisRoad, n):
        """
        运行车道上的车辆
        """
        # 如果循环过程中车道pop过则重新来一遍
        hasPop = True
        while hasPop:
            for index, c in enumerate(thisRoad.currentLane[n]):
                thisCar = c[0]

                # 该车已经调度完成则跳过这辆车
                if thisCar.flag == 'T':
                    continue

                pos = c[1]
                speed = min(thisRoad.limitSpeed, thisCar.maxSpeed)
                preCar = thisRoad.currentLane[n][index - 1][0] if index != 0 else None
                stopPos = preCar.currentLocPos if preCar else thisRoad.length + 1

                # 不超过前车或不出道路
                if pos + speed <= stopPos - 1:
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
                        # 如果不是预置车辆，在取下一条路之前先计算路况后再把下一条路push进route
                        if thisCar.isPreset:
                            pass
                        else:
                            nextCrossId = thisRoad.dstCross  # 取路的终点的路口id
                            # 如果即将到达终点则无需再加入路径
                            if nextCrossId != thisCar.dstCross:
                                goodRoadId = self.pickGoodRoad(nextCrossId, thisCar.dstCross, thisRoad.id)
                                i = thisCar.route.index(thisRoad.id)
                                if thisCar.route[-1] == thisRoad.id:
                                    thisCar.route.append(goodRoadId)

                        nextRoadId = thisCar.getNextRoadId()
                        if nextRoadId:
                            thisCar.flag = 'W'
                            direction = self.trafficMap.roadRelation[thisRoad.id][nextRoadId]

                            if direction == 'forward':
                                direnum = 0
                            elif direction == 'left':
                                direnum = 1
                            elif direction == 'right':
                                direnum = 2

                            hasPush = self.roads[nextRoadId].pushCarInwillEnter({
                                'car': thisCar,
                                's1': thisRoad.length - pos,
                                'preRoadId': thisCar.currentLocRoad,
                                'preLane': thisCar.currentLocLane,
                                'direnum': direnum,
                                'pos': thisCar.currentLocPos,
                                'laneNum': thisCar.currentLocLane,
                                'isPriority': thisCar.isPriority})

                        # 前方无路即已到达终点
                        else:
                            thisRoad.popCar(thisCar.id)
                            thisCar.flag = 'T'
                            thisCar.status = 'end'
                            thisCar.currentLocPos = thisRoad.length
                            self.endflag -= 1
                            MyLogger.print("剩余的未完成车辆：", self.endflag, '调度时间：', self.clock)
                            break  # 跳出本次循环并将重新循环，因为popCar以后循环次序变了

                # 检查调度完以后该车的调度状态
                if thisCar.flag == 'W':
                    self.existWaitCar = True

            # 没有pop过则不再重新循环
            else:
                hasPop = False

    def __runCarsInEntrance(self, thisRoad):
        """
        运行道路入口处车辆
        """
        while thisRoad.willEnter:
            # 道路入口处待入车辆优先级排序
            thisRoad.willEnter = sorted(thisRoad.willEnter, key=lambda x: (x['laneNum']), reverse=False)  # 车道编号
            thisRoad.willEnter = sorted(thisRoad.willEnter, key=lambda x: (x['pos']), reverse=True)  # 相对位置
            thisRoad.willEnter = sorted(thisRoad.willEnter, key=lambda x: (x['direnum']), reverse=False)  # 转向
            thisRoad.willEnter = sorted(thisRoad.willEnter, key=lambda x: (x['isPriority']), reverse=True)  # 是否优先

            # 取优先级最高的车
            item = thisRoad.willEnter.pop(0)
            thisCar = item['car']
            s1 = item['s1']
            preRoadId = item['preRoadId']
            preLane = item['preLane']
            preRoad = self.roads[preRoadId]

            hasPush, isWait = thisRoad.pushCar(thisCar, s1)

            # 进入道路成功
            if hasPush:
                self.cars[thisCar.id].flag = 'T'
                preRoad.popCar(thisCar.id)
                # 前道路的前车道的车再进行一次调度
                self.__runCarsInLane(preRoad, preLane)

            # 进入道路失败
            else:
                # 因受阻车为等待状态而进入失败
                if isWait:
                    pass  # 等待下一个大循环
                # 因没有位置或速度不够而进入失败
                else:
                    preRoad.currentLane[preLane][0][1] = preRoad.length
                    thisCar.currentLocPos = preRoad.length
                    thisCar.flag = 'T'

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
                for n in range(thisRoad.laneNum):
                    self.__runCarsInLane(thisRoad, n)

            # 优先车辆在此发车
            self.__startPriority()

            # 第二步：尝试将各自道路的入口处的车置入车道
            for roadId in self.roadSchedulOrder:
                thisRoad = self.roads[roadId]
                self.__runCarsInEntrance(thisRoad)
        return loop

    def run(self, clock=9999999):
        """
        运行调度器
        """
        self.__initSchedule()

        while self.endflag > 0:
            self.__initPeriod()

            loop = self.__runCars()

            self.__startCars()

            # print(self.clock,'Loop:', loop)
            # if self.clock >= clock:
            #     # self.showAllCarsInfo()
            #     self.showSomeRoadsInfo()
            #     # self.showAllRoadsInfo()
            #     input()

        return self.clock


def __loadPathTime(trafficMap, roads):
    """
    载入所有车辆的最短路径(测试用)
    """
    path = getShortestPath(trafficMap, roads)
    for carId in cars:
        thisCar = cars[carId]
        srcCross = thisCar.srcCross
        dstCross = thisCar.dstCross
        # thisCar.route = path[srcCross][dstCross]['path']
        thisCar.leaveTime = thisCar.planTime


def __loadPresetAnswer(presetAnswer_path, trafficMap, cars):
    """
    载入预置车辆的路径和实际出发时间
    """
    with open(presetAnswer_path, 'r') as f:
        f.readline()  # 跳过第一行
        for line in f:
            line = line.replace('(', '').replace(')', '').replace(' ', '').replace('\n', '')
            line = line.split(',')
            carId = line[0]
            leaveTime = int(line[1])
            route = line[2:]
            thisCar = cars[carId]
            thisCar.route = []
            crossId = thisCar.srcCross
            for r in route:
                thisCross = trafficMap.crossRelation[crossId].items()
                for next_crossId, roadId in thisCross:
                    if r == roadId[:-2]:
                        break
                thisCar.route.append(roadId)
                crossId = next_crossId
            thisCar.leaveTime = leaveTime


if __name__ == '__main__':
    from time import time

    t = time()

    configCrossPath = '../config/cross.txt'
    configRoadPath = '../config/road.txt'
    configCarPath = '../config/car.txt'
    presetAnswer_path = '../config/presetAnswer.txt'

    trafficMap = Map(configCrossPath, configRoadPath)
    roads = generateRoadInstances(configRoadPath)
    cars = generateCarInstances(configCarPath)

    __loadPathTime(trafficMap, roads)
    __loadPresetAnswer(presetAnswer_path, trafficMap, cars)

    cars = dict((carId, cars[carId]) for carId in cars if cars[carId].leaveTime <= 10)  # 筛选出发时间
    cars = dict((carId, cars[carId]) for carId in cars if cars[carId].maxSpeed >= 10)  # 筛选出发时间
    # cars = dict((carId,cars[carId]) for carId in cars if cars[carId].isPreset == 1) # 筛选是否预置
    # cars = dict((carId,cars[carId]) for i,carId in enumerate(cars) if i<1000) # 筛选车的数量
    # cars = dict((carId, cars[carId]) for i, carId in enumerate(cars) if i < 20000)  # 筛选车的数量

    scheduler = Scheduler(trafficMap, roads, cars)
    totalClock = scheduler.run(2000)

    MyLogger.print('Scheduling Clock:', totalClock)
    MyLogger.print('The Time Consumption:', time() - t)
    MyLogger.print('Car Num:', len(cars))
