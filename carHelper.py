# -*- coding:UTF-8 -*-
"""
@File    : carHelper.py
@Time    : 2019/3/12 19:14
@Author  : Blue Keroro
"""
import pandas as pd
import initialData


class carHelper(object):
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
    configPath = "CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataCar = pd.read_csv(configPath + '/car.csv')
    carHelperVar = carHelper(dataCar)
    print(carHelperVar.getCarIdList())
    print(carHelperVar.getCarFromByCarId(10013)
          , carHelperVar.getCarToByCarId(10013)
          , carHelperVar.getCarSpeedByCarId(10013)
          , carHelperVar.getCarPlanTimeByCarId(10013))
