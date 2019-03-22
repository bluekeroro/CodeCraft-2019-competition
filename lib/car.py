# -*- coding:UTF-8 -*-
"""
@File    : car.py
@Time    : 2019/3/12 19:14
@Author  : Blue Keroro
"""
import pandas as pd
from lib import initialData
from lib.myLogger import MyLogger


class Car(object):
    def __init__(self, carId):
        self.__carId = carId
        self.__currentSpeed = 0  # 初始车辆的速度为零
        self.__drivePath = list()  # 车辆已经行驶及正在行驶的路径
        if not (carId in Cars.getCarIdList()):
            raise RuntimeError("Invalid param.")

    def getCarId(self):
        """
        获取CarId
        :return:
        """
        return self.__carId

    def getCarFrom(self):
        """
        获取其始发地
        :return:
        """
        return Cars.getCarFromByCarId(self.__carId)

    def getCarTo(self):
        """
        获取其目的地
        :return:
        """
        return Cars.getCarToByCarId(self.__carId)

    def getCarLargestSpeed(self):
        """
        获取其最高速度
        :return:
        """
        return Cars.getCarLargestSpeedByCarId(self.__carId)

    def getCarPlanTime(self):
        """
        获取其出发时间
        :return:
        """
        return Cars.getCarPlanTimeByCarId(self.__carId)

    def getCarCurrentSpeed(self):
        """
        获取车辆当前速度
        :return:
        """
        return self.__currentSpeed

    def setCarCurrentSpeed(self, currentSpeed):
        """
        设置车辆当前速度
        :return:
        """
        if currentSpeed > self.getCarLargestSpeed():
            raise RuntimeError('Invalid param.')
        self.__currentSpeed = currentSpeed

    def addDriveRoad(self, roadId):
        """
        每进入一段路径，添加当前路径id
        :return:
        """
        self.__drivePath.append(roadId)

    def addDrivePath(self, path):
        """
        添加整段路径
        :param path: list
        :return:
        """
        self.__drivePath = path

    def getDrivePath(self):
        """
        获取车辆行驶的整段路径
        :return:
        """
        return self.__drivePath


class Cars(object):
    dataCar = None

    @classmethod
    def initial(cls, dataCar):
        cls.dataCar = dataCar

    @classmethod
    def getCarIdList(cls):
        """
        获取全部的carId
        :return: list类型
        """
        return list(cls.dataCar['id'])

    @classmethod
    def getCarFromByCarId(cls, carId):
        """
        根据carId获取其始发地
        :param carId:
        :return:
        """
        return list(cls.dataCar[cls.dataCar['id'] == carId]['from'])[0]

    @classmethod
    def getCarToByCarId(cls, carId):
        """
        根据carId获取其目的地
        :param carId:
        :return:
        """
        return list(cls.dataCar[cls.dataCar['id'] == carId]['to'])[0]

    @classmethod
    def getCarLargestSpeedByCarId(cls, carId):
        """
        根据carId获取其最高速度
        :param carId:
        :return:
        """
        return list(cls.dataCar[cls.dataCar['id'] == carId]['speed'])[0]

    @classmethod
    def getCarPlanTimeByCarId(cls, carId):
        """
        根据carId获取其出发时间
        :param carId:
        :return:
        """
        return list(cls.dataCar[cls.dataCar['id'] == carId]['planTime'])[0]

    @classmethod
    def getCarPlanTimeMin(cls):
        """
        获取全部数据的最小值
        :return:
        """
        return cls.dataCar['planTime'].min()

    @classmethod
    def getCarPlanTimeMax(cls):
        """
        获取全部数据的最大值
        :return:
        """
        return cls.dataCar['planTime'].max()

    @classmethod
    def getCarSpeedMin(cls):
        """
        获取全部数据的最小值
        :param carId:
        :return:
        """
        return cls.dataCar['Speed'].min()

    @classmethod
    def getCarSpeedMax(cls):
        """
        获取全部数据的最大值
        :return:
        """
        return cls.dataCar['Speed'].max()


if __name__ == "__main__":
    configPath = "../config"
    initialData.initial(configPath + "/car.txt", configPath + "/cross.txt", configPath + "/road.txt")
    # dataCar = pd.read_csv(configPath + '/car.csv')
    MyLogger.print(Cars.getCarIdList())
    MyLogger.print(Cars.getCarFromByCarId(10013)
                   , Cars.getCarToByCarId(10013)
                   , Cars.getCarLargestSpeedByCarId(10013)
                   , Cars.getCarPlanTimeByCarId(10013))
    carVar = Car(12047)
    MyLogger.print(carVar.getCarFrom()
                   , carVar.getCarTo()
                   , carVar.getCarLargestSpeed()
                   , carVar.getCarPlanTime())
    MyLogger.print('速度最小值', Cars.getCarSpeedMin(), '速度最大值', Cars.getCarSpeedMax())
    MyLogger.print('计划时间最小值', Cars.getCarPlanTimeMin(), '计划时间最大值', Cars.getCarPlanTimeMax())
