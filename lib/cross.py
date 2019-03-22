# -*- coding:UTF-8 -*-
"""
@File    : cross.py
@Time    : 2019/3/12 21:15
@Author  : Blue Keroro
"""
import pandas as pd
from lib import initialData
from lib.myLogger import MyLogger


class Cross(object):
    def __init__(self, crossId):
        self.__crossId = crossId
        if not (crossId in Crosses.getCrossIdList()):
            raise RuntimeError("Invalid param.")

    def getCrossId(self):
        """
        获取CrossId
        :return:
        """
        return self.__crossId

    def getUpRoadId(self):
        """
        获取上边路径的RoadId
        :param crossId:
        :return:
        """
        return Crosses.getUpRoadId(self.__crossId)

    def getRightRoadId(self):
        """
        获取右边路径的RoadId
        :param crossId:
        :return:
        """
        return Crosses.getRightRoadId(self.__crossId)

    def getDownRoadId(self):
        """
        获取下边路径的RoadId
        :param crossId:
        :return:
        """
        return Crosses.getDownRoadId(self.__crossId)

    def getLeftRoadId(self):
        """
        获取左边路径的RoadId
        :param crossId:
        :return:
        """
        return Crosses.getLeftRoadId(self.__crossId)


class Crosses(object):
    dataCross = None

    @classmethod
    def initial(cls, dataCross):
        cls.dataCross = dataCross

    @classmethod
    def getCrossIdList(cls):
        """
        获取全部的CrossId
        :return: list类型
        """
        return list(cls.dataCross['id'])

    @classmethod
    def getUpRoadId(cls, crossId):
        """
        根据crossId获取上边路径的RoadId
        :param crossId:
        :return:
        """
        return list(cls.dataCross[cls.dataCross['id'] == crossId]['roadId'])[0]

    @classmethod
    def getRightRoadId(cls, crossId):
        """
        根据crossId获取右边路径的RoadId
        :param crossId:
        :return:
        """
        return list(cls.dataCross[cls.dataCross['id'] == crossId]['roadId.1'])[0]

    @classmethod
    def getDownRoadId(cls, crossId):
        """
        根据crossId获取下边路径的RoadId
        :param crossId:
        :return:
        """
        return list(cls.dataCross[cls.dataCross['id'] == crossId]['roadId.2'])[0]

    @classmethod
    def getLeftRoadId(cls, crossId):
        """
        根据crossId获取左边路径的RoadId
        :param crossId:
        :return:
        """
        return list(cls.dataCross[cls.dataCross['id'] == crossId]['roadId.3'])[0]


if __name__ == '__main__':
    configPath = "../CodeCraft-2019/config_10"
    initialData.initial(configPath + "/car.txt", configPath + "/cross.txt", configPath + "/road.txt")
    dataCross = pd.read_csv(configPath + '/cross.csv')
    MyLogger.print(Crosses.getCrossIdList())
    MyLogger.print(Crosses.getUpRoadId(8), Crosses.getRightRoadId(8), Crosses.getDownRoadId(8),
                   Crosses.getLeftRoadId(8))
