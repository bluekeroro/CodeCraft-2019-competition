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
        self.carId = carId
        self.cares = cares
        if not (carId in cares.getCarIdList()):
            raise RuntimeError("Invalid param.")

    def getCarId(self):
        """
        获取CarId
        :return:
        """
        return self.carId

    def getCarFrom(self):
        """
        获取其始发地
        :return:
        """
        return self.cares.getCarFromByCarId(self.carId)

    def getCarTo(self):
        """
        获取其目的地
        :return:
        """
        return self.cares.getCarToByCarId(self.carId)

    def getCarSpeed(self):
        """
        获取其最高速度
        :return:
        """
        return self.cares.getCarSpeedByCarId(self.carId)

    def getCarPlanTime(self):
        """
        获取其出发时间
        :return:
        """
        return self.cares.getCarPlanTimeByCarId(self.carId)


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

    def getCarSpeedByCarId(self, carId):
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
          , caresVar.getCarSpeedByCarId(10013)
          , caresVar.getCarPlanTimeByCarId(10013))
    carVar = Car(12048, caresVar)
    print(carVar.getCarFrom()
          , carVar.getCarTo()
          , carVar.getCarSpeed()
          , carVar.getCarPlanTime())
