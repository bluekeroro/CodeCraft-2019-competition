# -*- coding:UTF-8 -*-
"""
@File    : road.py
@Time    : 2019/3/12 21:15
@Author  : Blue Keroro
"""
class Road(object):
    def __init__(self, roadId):
        self.__roadId = roadId
        if not (roadId in Roads.getRoadIdList()):
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
        return Roads.getRoadLengthByRoadId(self.__roadId)

    def getRoadLimitSpeed(self):
        """
        获取该路段的限速
        :return:
        """
        return Roads.getRoadLimitSpeedByRoadId(self.__roadId)

    def getRoadChannel(self):
        """
        获取该路段的车道数目
        :return:
        """
        return Roads.getRoadChannelByRoadId(self.__roadId)

    def getRoadFromCross(self):
        """
        获取该路段的起始点id
        :return:
        """
        return Roads.getRoadFromCrossByRoadId(self.__roadId)

    def getRoadToCross(self):
        """
        获取该路段的终点id
        :return:
        """
        return Roads.getRoadToCrossByRoadId(self.__roadId)

    def isDuplex(self):
        """
        判断该路段是否双向
        :return: 布尔类型
        """
        return Roads.isDuplexByRoadId(self.__roadId)

    def getAnotherCrossId(self, oldCrossId):
        return Roads.getAnotherCrossIdByRoadId(oldCrossId, self.__roadId)


class Roads(object):
    dataRoad = None

    @classmethod
    def initial(cls, dataRoad):
        cls.dataRoad = dataRoad

    @classmethod
    def getRoadIdList(cls):
        """
        获取全部的RoadId
        :return: list类型
        """
        return list(cls.dataRoad['id'])

    @classmethod
    def getRoadLengthByRoadId(cls, roadId):
        """
        根据roadId获取其长度
        :param roadId:
        :return:
        """
        return list(cls.dataRoad[cls.dataRoad['id'] == roadId]['length'].astype(int))[0]

    @classmethod
    def getRoadLimitSpeedByRoadId(cls, roadId):
        """
        根据roadId获取该路段的限速
        :param roadId:
        :return:
        """
        return list(cls.dataRoad[cls.dataRoad['id'] == roadId]['speed'])[0]

    @classmethod
    def getRoadChannelByRoadId(cls, roadId):
        """
        根据roadId获取该路段的车道数目
        :param roadId:
        :return:
        """
        return list(cls.dataRoad[cls.dataRoad['id'] == roadId]['channel'])[0]

    @classmethod
    def getRoadFromCrossByRoadId(cls, roadId):
        """
        根据roadId获取该路段的起始点id
        :param roadId:
        :return:
        """
        return list(cls.dataRoad[cls.dataRoad['id'] == roadId]['from'])[0]

    @classmethod
    def getRoadToCrossByRoadId(cls, roadId):
        """
        根据roadId获取该路段的终点id
        :param roadId:
        :return:
        """
        return list(cls.dataRoad[cls.dataRoad['id'] == roadId]['to'])[0]

    @classmethod
    def isDuplexByRoadId(cls, roadId):
        """
        根据roadId判断该路段是否双向
        :param roadId:
        :return: 布尔类型
        """
        if list(cls.dataRoad[cls.dataRoad['id'] == roadId]['isDuplex'])[0] == 1:
            return True
        else:
            return False

    @classmethod
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

    @classmethod
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
    from lib import initialData
    from lib.myLogger import MyLogger
    # 会报错，因为声明了静态类，不可直接运行该文件，需要在其他地方调用才可以
    configPath = "../CodeCraft-2019/config_10"
    initialData.initial(configPath + "/car.txt", configPath + "/cross.txt", configPath + "/road.txt")
    MyLogger.print(Roads.getRoadIdList())
    MyLogger.print(Roads.getRoadLengthByRoadId(5014)
                   , Roads.getRoadLimitSpeedByRoadId(5014)
                   , Roads.getRoadChannelByRoadId(5014)
                   , Roads.getRoadFromCrossByRoadId(5014)
                   , Roads.getRoadToCrossByRoadId(5014)
                   , Roads.isDuplexByRoadId(5014))
    roadIdList = [5000, 5006, 5012, 5018, 5023, 5024, 5030, 5036, 5042, 5052]
    MyLogger.print(Roads.getSumRoadLength(roadIdList))
