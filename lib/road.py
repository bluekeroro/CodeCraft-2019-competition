# -*- coding:UTF-8 -*-
"""
@File    : road.py
@Time    : 2019/3/12 21:15
@Author  : Blue Keroro
"""
import pandas as pd
from lib import initialData


class Road(object):
    def __init__(self, roadId, roads):
        self.__roadId = roadId
        self.__roads = roads
        if not (roadId in roads.getRoadIdList()):
            raise RuntimeError("Invalid param.")

    def getRoadId(self):
        """
        获取RoadId
        :return:
        """
        return self.__roadId

    def getRoadLength(self):
        """
        获取其长度
        :return:
        """
        return self.__roads.getRoadLengthByRoadId(self.__roadId)

    def getRoadLimitSpeed(self):
        """
        获取该路段的限速
        :return:
        """
        return self.__roads.getRoadLimitSpeedByRoadId(self.__roadId)

    def getRoadChannel(self):
        """
        获取该路段的车道数目
        :return:
        """
        return self.__roads.getRoadChannelByRoadId(self.__roadId)

    def getRoadFromCross(self):
        """
        获取该路段的起始点id
        :return:
        """
        return self.__roads.getRoadFromCrossByRoadId(self.__roadId)

    def getRoadToCross(self):
        """
        获取该路段的终点id
        :return:
        """
        return self.__roads.getRoadToCrossByRoadId(self.__roadId)

    def isDuplex(self):
        """
        判断该路段是否双向
        :return: 布尔类型
        """
        return self.__roads.isDuplexByRoadId(self.__roadId)

    def getAnotherCrossId(self, oldCrossId):
        return self.__roads.getAnotherCrossIdByRoadId(oldCrossId, self.__roadId)


class Roads(object):
    def __init__(self, dataRoad):
        self.dataRoad = dataRoad

    def getRoadIdList(self):
        """
        获取全部的RoadId
        :return: list类型
        """
        return list(self.dataRoad['id'])

    def getRoadLengthByRoadId(self, roadId):
        """
        根据roadId获取其长度
        :param roadId:
        :return:
        """
        return list(self.dataRoad[self.dataRoad['id'] == roadId]['length'].astype(int))[0]

    def getRoadLimitSpeedByRoadId(self, roadId):
        """
        根据roadId获取该路段的限速
        :param roadId:
        :return:
        """
        return list(self.dataRoad[self.dataRoad['id'] == roadId]['speed'])[0]

    def getRoadChannelByRoadId(self, roadId):
        """
        根据roadId获取该路段的车道数目
        :param roadId:
        :return:
        """
        return list(self.dataRoad[self.dataRoad['id'] == roadId]['channel'])[0]

    def getRoadFromCrossByRoadId(self, roadId):
        """
        根据roadId获取该路段的起始点id
        :param roadId:
        :return:
        """
        return list(self.dataRoad[self.dataRoad['id'] == roadId]['from'])[0]

    def getRoadToCrossByRoadId(self, roadId):
        """
        根据roadId获取该路段的终点id
        :param roadId:
        :return:
        """
        return list(self.dataRoad[self.dataRoad['id'] == roadId]['to'])[0]

    def isDuplexByRoadId(self, roadId):
        """
        根据roadId判断该路段是否双向
        :param roadId:
        :return: 布尔类型
        """
        if list(self.dataRoad[self.dataRoad['id'] == roadId]['isDuplex'])[0] == 1:
            return True
        else:
            return False

    def getAnotherCrossIdByRoadId(self, oldCrossId, roadId):
        """
        获取路径另一端的crossId
        :param oldCrossId:
        :param roadId:
        :return:
        """
        toVar = self.getRoadToCrossByRoadId(roadId)
        fromVar = self.getRoadFromCrossByRoadId(roadId)
        return fromVar if oldCrossId == toVar else toVar

    def getSumRoadLength(self, roadIdList):
        """
        计算一连串路径的长度之和
        :param roadIdList: list
        :return:
        """
        ret = 0
        for roadId in roadIdList:
            ret += self.getRoadLengthByRoadId(roadId)
        return ret


if __name__ == '__main__':
    configPath = "../CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataRoad = pd.read_csv(configPath + '/road.csv')
    roadsVar = Roads(dataRoad)
    print(roadsVar.getRoadIdList())
    print(roadsVar.getRoadLengthByRoadId(5014)
          , roadsVar.getRoadLimitSpeedByRoadId(5014)
          , roadsVar.getRoadChannelByRoadId(5014)
          , roadsVar.getRoadFromCrossByRoadId(5014)
          , roadsVar.getRoadToCrossByRoadId(5014)
          , roadsVar.isDuplexByRoadId(5014))
    roadIdList = [5000, 5006, 5012, 5018, 5023, 5024, 5030, 5036, 5042, 5052]
    print(roadsVar.getSumRoadLength(roadIdList))
