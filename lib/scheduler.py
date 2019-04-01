# -*- coding:UTF-8 -*-

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

    def showAllCarsInfo(self):
        for carId in sorted(self.cars.keys()):
            thisCar = self.cars[carId]
            print(carId, thisCar.status, thisCar.flag)

    def showAllRoadsInfo(self):
        for roadId in sorted(self.roads.keys()):
            thisRoad = self.roads[roadId]
            for n in range(thisRoad.laneNum):
                print(roadId, [(c[0].id,c[1]) for c in thisRoad.currentLane[n]])
            print('')

    def __loadShortestPath(self, graph):
        """
        载入所有车辆的最短路径
        """
        path = getShortestPath(self.trafficMap, self.roads, self.cars)
        for carId in self.cars:
            thisCar = self.cars[carId]
            srcCross = thisCar.srcCross
            dstCross = thisCar.dstCross
            thisCar.route = path[srcCross][dstCross]['path']

    def __loadLeaveTime(self):
        """
        载入所有车辆的实际出发时间
        """
        for carId in self.cars:
            thisCar = self.cars[carId]
            thisCar.leaveTime = thisCar.planTime # 先把实际出发时间载入为计划出发时间

    def __initSchedule(self):
        """
        调度初始化
        """
        graph = self.__getNetwork()
        self.__loadShortestPath(graph)
        self.__loadLeaveTime()

        self.clock = 0
        for carId in sorted(self.cars.keys()):
            self.cars[carId].status = 'start'
            self.startQueue.put(carId)

    def __initPeriod(self):
        """
        周期初始化
        """
        self.clock += 1
        for roadId in self.roads:
            for n in range(self.roads[roadId].laneNum):
                for carId,pos in self.roads[roadId].currentLane[n]:
                    self.cars[carId].flag = 'W'

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
                hasPush = thisRoad.pushCar(thisCar, 0)
                # 进入道路成功
                if hasPush:
                    self.cars[carId].status = 'run'
                    self.cars[carId].flag = 'T'
                # 因为没位置而进入道路失败
                else:
                    self.startQueue.put(carId)
            # 时钟尚未过出发时间
            else:
                self.startQueue.put(carId)

    # def __runCars(self):
    #     """
    #     调度路上的车辆
    #     """
    #     for roadId in sorted(self.roads.keys()):
    #         thisRoad = self.roads[roadId]
    #         for n in range(thisRoad.laneNum):
    #             for index, carIdPos in enumerate(thisRoad.currentLane[n]):
    #                 carId = carIdPos[0]
    #                 pos = carIdPos[1]
    #                 if index == 0:
                        
    #                 # frontCarId = thisRoad.currentLane[n][index-1][0] if index>0 else None

    #                 print(roadId,carId,pos,frontCarId)
    #         print('')


    def run(self):
        """
        运行调度器
        """
        self.__initSchedule()

        for x in range(1):
            
            self.__initPeriod()

            # self.__runCars()

            self.__startCars()

            self.showAllCarsInfo()
            self.showAllRoadsInfo()




if __name__ == '__main__':
    configCrossPath = '../config/cross.txt'
    configRoadPath = '../config/road.txt'
    configCarPath = '../config/car.txt'

    trafficMap = Map(configCrossPath, configRoadPath)
    roads = road.generateRoadInstances(configRoadPath)
    cars = car.generateCarInstances(configCarPath)

    scheduler = Scheduler(trafficMap, roads, cars)
    scheduler.run()
