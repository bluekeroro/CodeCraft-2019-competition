# -*- coding:UTF-8 -*-
"""
@File    : road.py
@Time    : 2019/3/12 21:15
@Author  : Blue Keroro
"""
import pandas as pd
from lib import initialData


class Road(object):
    def __init__(self, roadId, roades):
        self.roadId = roadId
        self.roades = roades
        if not (roadId in roades.getRoadIdList()):
            raise RuntimeError("Invalid param.")

    def getRoadId(self):
        """
        获取RoadId
        :return:
        """
        return self.roadId

    def getRoadLength(self):
        """
        获取其长度
        :return:
        """
        return self.roades.getRoadLengthByRoadId(self.roadId)

    def getRoadSpeed(self):
        """
        获取该路段的限速
        :return:
        """
        return self.roades.getRoadSpeedByRoadId(self.roadId)

    def getRoadChannel(self):
        """
        获取该路段的车道数目
        :return:
        """
        return self.roades.getRoadChannelByRoadId(self.roadId)

    def getRoadFromCross(self):
        """
        获取该路段的起始点id
        :return:
        """
        return self.roades.getRoadFromCrossByRoadId(self.roadId)

    def getRoadToCross(self):
        """
        获取该路段的终点id
        :return:
        """
        return self.roades.getRoadToCrossByRoadId(self.roadId)

    def isDuplex(self):
        """
        判断该路段是否双向
        :return: 布尔类型
        """
        return self.roades.isDuplexByRoadId(self.roadId)

    def getAnotherCrossId(self, oldCrossId):
        return self.roades.getAnotherCrossIdByRoadId(oldCrossId, self.roadId)


class Roades(object):
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

    def getRoadSpeedByRoadId(self, roadId):
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


if __name__ == '__main__':
    configPath = "../CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataRoad = pd.read_csv(configPath + '/road.csv')
    roadesVar = Roades(dataRoad)
    print(roadesVar.getRoadIdList())
    print(roadesVar.getRoadLengthByRoadId(5014)
          , roadesVar.getRoadSpeedByRoadId(5014)
          , roadesVar.getRoadChannelByRoadId(5014)
          , roadesVar.getRoadFromCrossByRoadId(5014)
          , roadesVar.getRoadToCrossByRoadId(5014)
          , roadesVar.isDuplexByRoadId(5014))
