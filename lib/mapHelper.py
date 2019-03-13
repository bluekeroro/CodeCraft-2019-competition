# -*- coding:UTF-8 -*-
"""
@File    : mapHelper.py
@Time    : 2019/3/10 19:54
@Author  : Blue Keroro
"""
import matplotlib.pyplot as plt
import pandas as pd
from lib import initialData
from lib.cross import Crosses
from lib.road import Roades


class MapHelper(object):
    def __init__(self, dataCross, dataRoad):
        """
        :param dataCross: dataFrame cross数据
        :param dataRoad: dataFrame road数据
        """
        self.crosses = Crosses(dataCross)
        self.roades = Roades(dataRoad)
        self.hasAddMap = {}
        self.interval = 20
        self.font1 = {'family': 'Times New Roman',
                      'weight': 'normal',
                      'size': 10,
                      }

    def getRoadIdByDirection(self, crossId, direction):
        """
        根据方向获取cross的四条通路，不可通行则返回-1
        :param crossId:
        :param direction: String 方向 {up,right,down,left}
        :return:
        """
        roadId = None
        if direction == 'up':
            roadId = self.crosses.getUpRoadId(crossId)
        elif direction == 'right':
            roadId = self.crosses.getRightRoadId(crossId)
        elif direction == 'down':
            roadId = self.crosses.getDownRoadId(crossId)
        elif direction == 'left':
            roadId = self.crosses.getLeftRoadId(crossId)
        if roadId is None or roadId == -1:
            return -1
        if (not self.roades.isDuplexByRoadId(roadId)) and self.roades.getRoadFromCrossByRoadId(roadId) != crossId:
            return -1
        return roadId

    def addArrow(self, crossId, roadId, x, y, newX, newY):
        """
        绘制箭头函数，可判断若不符合可行驶方向，则不绘制
        :param crossId: 为空时则直接画箭头
        :param roadId: 为空时则直接画箭头
        :param x: 箭头起始坐标
        :param y: 箭头起始坐标
        :param newX: 箭头终点坐标
        :param newY: 箭头终点坐标
        :return:
        """
        width = 0.3
        head_width = 6 * width # 3
        head_length = 2.5 * head_width # 1.5
        if (crossId is None or roadId is None) \
                or (self.roades.getRoadFromCrossByRoadId(roadId) is crossId or self.roades.isDuplexByRoadId(roadId)):
            plt.arrow(x, y, newX - x, newY - y, color='r', width=width, head_width=head_width, head_length=head_length,
                      length_includes_head=True)

    def __dfs(self, x, y, crossId):
        if crossId in self.hasAddMap:
            return
        plt.scatter(x, y, color='', marker='o', edgecolors='g', s=200)
        plt.text(x, y, crossId)
        self.hasAddMap[crossId] = True
        upRoadId = self.crosses.getUpRoadId(crossId)
        rightRoadId = self.crosses.getRightRoadId(crossId)
        downRoadId = self.crosses.getDownRoadId(crossId)
        leftRoadId = self.crosses.getLeftRoadId(crossId)
        if upRoadId != -1:
            newX = x
            newY = y + self.interval
            self.addArrow(crossId, upRoadId, x, y, newX, newY)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.roades.getAnotherCrossIdByRoadId(crossId, upRoadId))
            plt.text((newX + x) / 2, (newY + y) / 2,
                     str(upRoadId) + '(' + str(self.roades.getRoadLengthByRoadId(upRoadId)) + ')',
                     fontdict=self.font1)
            self.__dfs(newX, newY, self.roades.getAnotherCrossIdByRoadId(crossId, upRoadId))
        if rightRoadId != -1:
            newX = x + self.interval
            newY = y
            self.addArrow(crossId, rightRoadId, x, y, newX, newY)
            plt.text((newX + x) / 2, (newY + y) / 2,
                     str(rightRoadId) + '(' + str(self.roades.getRoadLengthByRoadId(rightRoadId)) + ')',
                     fontdict=self.font1)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.roades.getAnotherCrossIdByRoadId(crossId, rightRoadId))
            self.__dfs(newX, newY, self.roades.getAnotherCrossIdByRoadId(crossId, rightRoadId))
        if downRoadId != -1:
            newX = x
            newY = y - self.interval
            self.addArrow(crossId, downRoadId, x, y, newX, newY)
            plt.text((newX + x) / 2, (newY + y) / 2,
                     str(downRoadId) + '(' + str(self.roades.getRoadLengthByRoadId(downRoadId)) + ')',
                     fontdict=self.font1)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.roades.getAnotherCrossIdByRoadId(crossId, downRoadId))
            self.__dfs(newX, newY, self.roades.getAnotherCrossIdByRoadId(crossId, downRoadId))
        if leftRoadId != -1:
            newX = x - self.interval
            newY = y
            self.addArrow(crossId, leftRoadId, x, y, newX, newY)
            plt.text((newX + x) / 2, (newY + y) / 2,
                     str(leftRoadId) + '(' + str(self.roades.getRoadLengthByRoadId(leftRoadId)) + ')',
                     fontdict=self.font1)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.roades.getAnotherCrossIdByRoadId(crossId, leftRoadId))
            self.__dfs(newX, newY, self.roades.getAnotherCrossIdByRoadId(crossId, leftRoadId))

    def plotMap(self):
        """
        绘制地图，由于路段长短弯直不一，无法精确绘制。
        绘制各点距离暂定为self.interval.在自带的10张地图没有出现问题。
        :return:
        """
        self.__dfs(0, 0, self.crosses.getCrossIdList()[0])
        plt.show()


if __name__ == "__main__":
    configPath = "../CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    mapHelperVar = MapHelper(dataCross, dataRoad)
    print(mapHelperVar.crosses.getCrossIdList())
    print(mapHelperVar.crosses.getCrossIdList()[10])
    print(mapHelperVar.getRoadIdByDirection(10, 'up')
          , mapHelperVar.getRoadIdByDirection(10, 'right')
          , mapHelperVar.getRoadIdByDirection(10, 'down')
          , mapHelperVar.getRoadIdByDirection(10, 'left'))
    mapHelperVar.plotMap()
