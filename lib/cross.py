# -*- coding:UTF-8 -*-
"""
@File    : cross.py
@Time    : 2019/3/12 21:15
@Author  : Blue Keroro
"""
import pandas as pd
from lib import initialData


class Cross(object):
    def __init__(self, crossId, crosses):
        self.__crossId = crossId
        self.__crosses = crosses
        if not (crossId in crosses.getCrossIdList()):
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
        return self.__crosses.getUpRoadId(self.__crossId)

    def getRightRoadId(self):
        """
        获取右边路径的RoadId
        :param crossId:
        :return:
        """
        return self.__crosses.getRightRoadId(self.__crossId)

    def getDownRoadId(self):
        """
        获取下边路径的RoadId
        :param crossId:
        :return:
        """
        return self.__crosses.getDownRoadId(self.__crossId)

    def getLeftRoadId(self):
        """
        获取左边路径的RoadId
        :param crossId:
        :return:
        """
        return self.__crosses.getLeftRoadId(self.__crossId)


class Crosses(object):
    def __init__(self, dataCross):
        self.dataCross = dataCross

    def getCrossIdList(self):
        """
        获取全部的CrossId
        :return: list类型
        """
        return list(self.dataCross['id'])

    def getUpRoadId(self, crossId):
        """
        根据crossId获取上边路径的RoadId
        :param crossId:
        :return:
        """
        return list(self.dataCross[self.dataCross['id'] == crossId]['roadId'])[0]

    def getRightRoadId(self, crossId):
        """
        根据crossId获取右边路径的RoadId
        :param crossId:
        :return:
        """
        return list(self.dataCross[self.dataCross['id'] == crossId]['roadId.1'])[0]

    def getDownRoadId(self, crossId):
        """
        根据crossId获取下边路径的RoadId
        :param crossId:
        :return:
        """
        return list(self.dataCross[self.dataCross['id'] == crossId]['roadId.2'])[0]

    def getLeftRoadId(self, crossId):
        """
        根据crossId获取左边路径的RoadId
        :param crossId:
        :return:
        """
        return list(self.dataCross[self.dataCross['id'] == crossId]['roadId.3'])[0]


if __name__ == '__main__':
    configPath = "../CodeCraft-2019/config_10"
    initialData.initial(configPath+"/car.txt",configPath+"/cross.txt",configPath+"/road.txt")
    dataCross = pd.read_csv(configPath + '/cross.csv')
    crossesVar = Crosses(dataCross)
    print(crossesVar.getCrossIdList())
    print(crossesVar.getUpRoadId(8), crossesVar.getRightRoadId(8), crossesVar.getDownRoadId(8),
          crossesVar.getLeftRoadId(8))
