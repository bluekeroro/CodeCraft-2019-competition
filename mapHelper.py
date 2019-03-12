# -*- coding:UTF-8 -*-
"""
@File    : mapHelper.py
@Time    : 2019/3/10 19:54
@Author  : Blue Keroro
"""
import matplotlib.pyplot as plt
import pandas as pd
import initialData


class mapHelper(object):
    def __init__(self, dataCross, dataRoad):
        """
        :param dataCross: dataFrame cross数据
        :param dataRoad: dataFrame road数据
        """
        self.hasAddMap = {}
        self.dataRoad = dataRoad
        self.dataCross = dataCross
        self.interval = 20
        self.font1 = {'family': 'Times New Roman',
                      'weight': 'normal',
                      'size': 10,
                      }

    def getRoadLength(self, roadId):
        """
        根据roadId获取其长度
        :param roadId:
        :return:
        """
        return list(self.dataRoad[self.dataRoad['id'] == roadId]['length'].astype(int))[0]

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

    def getNewCrossIdByRoadId(self, oldCrossId, roadId):
        """
        根据oldCrossId以及roadId获取该路段的另一个端点CrossId
        :param oldCrossId:
        :param roadId:
        :return:
        """
        dfTemp = self.dataCross[
            (self.dataCross['roadId'] == roadId) | (self.dataCross['roadId.1'] == roadId) |
            (self.dataCross['roadId.2'] == roadId) | (self.dataCross['roadId.3'] == roadId)
            ]
        dfTemp = dfTemp[dfTemp['id'] != oldCrossId]
        return list(dfTemp['id'])[0]

    def getSpeedByRoadId(self, roadId):
        """
        根据roadId获取该路段的限速
        :param roadId:
        :return:
        """
        return list(self.dataRoad[self.dataRoad['id'] == roadId]['speed'])[0]

    def __dfs(self, x, y, oldX, oldY, crossId, roadId):
        if crossId in self.hasAddMap:
            return
        plt.scatter(x, y, color='', marker='o', edgecolors='g', s=200)
        plt.text(x, y, crossId)
        self.hasAddMap[crossId] = True
        upRoadId = self.getUpRoadId(crossId)
        rightRoadId = self.getRightRoadId(crossId)
        downRoadId = self.getDownRoadId(crossId)
        leftRoadId = self.getLeftRoadId(crossId)
        if upRoadId != -1:
            newX = x
            newY = y + self.interval
            plt.plot([newX, x], [newY, y], color='r')
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.getNewCrossIdByRoadId(crossId, upRoadId))
            plt.text((newX + x) / 2, (newY + y) / 2, str(upRoadId) + '(' + str(self.getRoadLength(upRoadId)) + ')',
                     fontdict=self.font1)
            self.__dfs(newX, newY, x, y, self.getNewCrossIdByRoadId(crossId, upRoadId), upRoadId)
        if rightRoadId != -1:
            newX = x + self.interval
            newY = y
            plt.plot([newX, x], [newY, y], color='r')
            plt.text((newX + x) / 2, (newY + y) / 2,
                     str(rightRoadId) + '(' + str(self.getRoadLength(rightRoadId)) + ')', fontdict=self.font1)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.getNewCrossIdByRoadId(crossId, rightRoadId))
            self.__dfs(newX, newY, x, y, self.getNewCrossIdByRoadId(crossId, rightRoadId), rightRoadId)
        if downRoadId != -1:
            newX = x
            newY = y - self.interval
            plt.plot([newX, x], [newY, y], color='r')
            plt.text((newX + x) / 2, (newY + y) / 2, str(downRoadId) + '(' + str(self.getRoadLength(downRoadId)) + ')',
                     fontdict=self.font1)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.getNewCrossIdByRoadId(crossId, downRoadId))
            self.__dfs(newX, newY, x, y, self.getNewCrossIdByRoadId(crossId, downRoadId), downRoadId)
        if leftRoadId != -1:
            newX = x - self.interval
            newY = y
            plt.plot([newX, x], [newY, y], color='r')
            plt.text((newX + x) / 2, (newY + y) / 2, str(leftRoadId) + '(' + str(self.getRoadLength(leftRoadId)) + ')',
                     fontdict=self.font1)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.getNewCrossIdByRoadId(crossId, leftRoadId))
            self.__dfs(newX, newY, x, y, self.getNewCrossIdByRoadId(crossId, leftRoadId), leftRoadId)

    def plotMap(self):
        """
        绘制地图，由于路段长短弯直不一，无法精确绘制。
        绘制各点距离暂定为self.interval.在自带的10张地图没有出现问题。
        :return:
        """
        x = 0
        y = 0
        plt.scatter(x, y, color='', marker='o', edgecolors='g', s=200)
        plt.text(x, y, self.dataCross['id'][0].astype(int))
        self.hasAddMap[self.dataCross['id'][0].astype(int)] = True
        crossId = self.dataCross['id'][0].astype(int)
        upRoadId = self.getUpRoadId(crossId)
        rightRoadId = self.getRightRoadId(crossId)
        downRoadId = self.getDownRoadId(crossId)
        leftRoadId = self.getLeftRoadId(crossId)
        if upRoadId != -1:
            newX = x
            newY = y + self.interval
            plt.plot([newX, x], [newY, y], color='r')
            plt.text((newX + x) / 2, (newY + y) / 2, str(upRoadId) + '(' + str(self.getRoadLength(upRoadId)) + ')',
                     fontdict=self.font1)
            self.__dfs(newX, newY, x, y,
                       self.getNewCrossIdByRoadId(self.dataCross['id'][0].astype(int), upRoadId), upRoadId)
        if rightRoadId != -1:
            newX = x + self.interval
            newY = y
            plt.plot([newX, x], [newY, y], color='r')
            plt.text((newX + x) / 2, (newY + y) / 2,
                     str(rightRoadId) + '(' + str(self.getRoadLength(rightRoadId)) + ')', fontdict=self.font1)
            self.__dfs(newX, newY, x, y,
                       self.getNewCrossIdByRoadId(self.dataCross['id'][0].astype(int), rightRoadId), rightRoadId)
        if downRoadId != -1:
            newX = x
            newY = y - self.interval
            plt.plot([newX, x], [newY, y], color='r')
            plt.text((newX + x) / 2, (newY + y) / 2, str(downRoadId) + '(' + str(self.getRoadLength(downRoadId)) + ')',
                     fontdict=self.font1)
            self.__dfs(x, newY, x, y,
                       self.getNewCrossIdByRoadId(self.dataCross['id'][0].astype(int), downRoadId), downRoadId)
        if leftRoadId != -1:
            newX = x - self.interval
            newY = y
            plt.plot([newX, x], [newY, y], color='r')
            plt.text((newX + x) / 2, (newY + y) / 2, str(leftRoadId) + '(' + str(self.getRoadLength(leftRoadId)) + ')',
                     fontdict=self.font1)
            self.__dfs(newX, newY, x, y,
                       self.getNewCrossIdByRoadId(self.dataCross['id'][0].astype(int), leftRoadId), leftRoadId)
        plt.show()


if __name__ == "__main__":
    configPath = "CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    mapHelperVar = mapHelper(dataCross, dataRoad)
    print(mapHelperVar.getUpRoadId(8), mapHelperVar.getRightRoadId(8), mapHelperVar.getDownRoadId(8),
          mapHelperVar.getLeftRoadId(8))
    print(mapHelperVar.getSpeedByRoadId(5012), mapHelperVar.getSpeedByRoadId(5013))
    mapHelperVar.plotMap()
