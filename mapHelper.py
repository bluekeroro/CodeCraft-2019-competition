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
        self.hasAddMap = {}
        self.dataRoad = dataRoad
        self.dataCross = dataCross
        self.interval = 10

    def getRoadLength(self, roadId):
        return list(self.dataRoad[self.dataRoad['id'] == roadId]['length'].astype(int))[0]

    def getUpRoadId(self, crossId):
        return list(self.dataCross[self.dataCross['id'] == crossId]['roadId'])[0]

    def getRightRoadId(self, crossId):
        return list(self.dataCross[self.dataCross['id'] == crossId]['roadId.1'])[0]

    def getDownRoadId(self, crossId):
        return list(self.dataCross[self.dataCross['id'] == crossId]['roadId.2'])[0]

    def getLeftRoadId(self, crossId):
        return list(self.dataCross[self.dataCross['id'] == crossId]['roadId.3'])[0]

    def getNewCrossIdByRoadId(self, oldCrossId, roadId):
        dfTemp = self.dataCross[
            (self.dataCross['roadId'] == roadId) | (self.dataCross['roadId.1'] == roadId) |
            (self.dataCross['roadId.2'] == roadId) | (self.dataCross['roadId.3'] == roadId)
            ]
        dfTemp = dfTemp[dfTemp['id'] != oldCrossId]
        return list(dfTemp['id'])[0]

    def __dfs(self, x, y, oldX, oldY, crossId, roadId):
        if crossId in self.hasAddMap:
            return
        # print('x=', x, 'y=', y, 'crossId=', crossId)

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
            # plt.text((newX + x) / 2, (newY + y) / 2, roadId)
            self.__dfs(newX, newY, x, y, self.getNewCrossIdByRoadId(crossId, upRoadId), upRoadId)
        if rightRoadId != -1:
            newX = x + self.interval
            newY = y
            plt.plot([newX, x], [newY, y], color='r')
            # plt.text((newX + x) / 2, (newY + y) / 2, roadId)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.getNewCrossIdByRoadId(crossId, rightRoadId))
            self.__dfs(newX, newY, x, y, self.getNewCrossIdByRoadId(crossId, rightRoadId), rightRoadId)
        if downRoadId != -1:
            newX = x
            newY = y - self.interval
            plt.plot([newX, x], [newY, y], color='r')
            # plt.text((newX + x) / 2, (newY + y) / 2, roadId)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.getNewCrossIdByRoadId(crossId, downRoadId))
            self.__dfs(newX, newY, x, y, self.getNewCrossIdByRoadId(crossId, downRoadId), downRoadId)
        if leftRoadId != -1:
            newX = x - self.interval
            newY = y
            plt.plot([newX, x], [newY, y], color='r')
            # plt.text((newX + x) / 2, (newY + y) / 2, roadId)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.getNewCrossIdByRoadId(crossId, leftRoadId))
            self.__dfs(newX, newY, x, y, self.getNewCrossIdByRoadId(crossId, leftRoadId), leftRoadId)

    def plotMap(self):
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
            self.__dfs(newX, newY, x, y,
                     self.getNewCrossIdByRoadId(self.dataCross['id'][0].astype(int), upRoadId), upRoadId)
        if rightRoadId != -1:
            newX = x + self.interval
            newY = y
            plt.plot([newX, x], [newY, y], color='r')
            self.__dfs(newX, newY, x, y,
                     self.getNewCrossIdByRoadId(self.dataCross['id'][0].astype(int), rightRoadId), rightRoadId)
        if downRoadId != -1:
            newX = x
            newY = y - self.interval
            plt.plot([newX, x], [newY, y], color='r')
            self.__dfs(x, newY, x, y,
                     self.getNewCrossIdByRoadId(self.dataCross['id'][0].astype(int), downRoadId), downRoadId)
        if leftRoadId != -1:
            newX = x - self.interval
            newY = y
            plt.plot([newX, x], [newY, y], color='r')
            self.__dfs(newX, newY, x, y,
                     self.getNewCrossIdByRoadId(self.dataCross['id'][0].astype(int), leftRoadId), leftRoadId)

        plt.show()


if __name__ == "__main__":
    configPath = "CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    # print(getUpRoadId(8),getRightRoadId(8),getDownRoadId(8),getLeftRoadId(8))
    mapHelper(dataCross, dataRoad).plotMap()
