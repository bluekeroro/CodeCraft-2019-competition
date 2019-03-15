# -*- coding:UTF-8 -*-
"""
@File    : car.py
@Time    : 2019/3/12 19:14
@Author  : Blue Keroro
"""
import pandas as pd
from lib import initialData


class Car(object):
    def __init__(self, carId, cares):
        self.__carId = carId
        self.__cares = cares
        self.__currentSpeed = 0  # 初始车辆的速度为零
        self.__drivePath = list()  # 车辆已经行驶及正在行驶的路径
        if not (carId in cares.getCarIdList()):
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
        return self.__cares.getCarFromByCarId(self.__carId)

    def getCarTo(self):
        """
        获取其目的地
        :return:
        """
        return self.__cares.getCarToByCarId(self.__carId)

    def getCarLargestSpeed(self):
        """
        获取其最高速度
        :return:
        """
        return self.__cares.getCarLargestSpeedByCarId(self.__carId)

    def getCarPlanTime(self):
        """
        获取其出发时间
        :return:
        """
        return self.__cares.getCarPlanTimeByCarId(self.__carId)

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

    def addDrivePath(self, roadId):
        """
        每进入一段路径，添加当前路径id
        :return:
        """
        self.__drivePath.append(roadId)


class Cares(object):
    def __init__(self, dataCar):
        self.dataCar = dataCar

    def getCarIdList(self):
        """
        获取全部的carId
        :return: list类型
        """
        return list(self.dataCar['id'])

    def getCarFromByCarId(self, carId):
        """
        根据carId获取其始发地
        :param carId:
        :return:
        """
        return list(self.dataCar[self.dataCar['id'] == carId]['from'])[0]

    def getCarToByCarId(self, carId):
        """
        根据carId获取其目的地
        :param carId:
        :return:
        """
        return list(self.dataCar[self.dataCar['id'] == carId]['to'])[0]

    def getCarLargestSpeedByCarId(self, carId):
        """
        根据carId获取其最高速度
        :param carId:
        :return:
        """
        return list(self.dataCar[self.dataCar['id'] == carId]['speed'])[0]

    def getCarPlanTimeByCarId(self, carId):
        """
        根据carId获取其出发时间
        :param carId:
        :return:
        """
        return list(self.dataCar[self.dataCar['id'] == carId]['planTime'])[0]


if __name__ == "__main__":
    configPath = "../CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataCar = pd.read_csv(configPath + '/car.csv')
    caresVar = Cares(dataCar)
    print(caresVar.getCarIdList())
    print(caresVar.getCarFromByCarId(10013)
          , caresVar.getCarToByCarId(10013)
          , caresVar.getCarLargestSpeedByCarId(10013)
          , caresVar.getCarPlanTimeByCarId(10013))
    carVar = Car(12048, caresVar)
    print(carVar.getCarFrom()
          , carVar.getCarTo()
          , carVar.getCarLargestSpeed()
          , carVar.getCarPlanTime())
