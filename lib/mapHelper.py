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
from lib.road import Roads
import networkx as nx

from lib_fqy.map import Map
from lib_fqy.road import generateRoadInstances


class MapHelper(object):
    def __init__(self, dataCross, dataRoad):
        """
        :param dataCross: dataFrame cross数据
        :param dataRoad: dataFrame road数据
        """
        self.crosses = Crosses(dataCross)
        self.roads = Roads(dataRoad)
        self.hasAddMap = {}
        self.interval = 20
        self.font1 = {'family': 'Times New Roman',
                      'weight': 'normal',
                      'size': 10,
                      }
        self.graph = None

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
        if (not self.roads.isDuplexByRoadId(roadId)) and self.roads.getRoadFromCrossByRoadId(roadId) != crossId:
            return -1
        return roadId

    def getRoadIdByTwoCrossIds(self, crossId1, crossId2):
        """
        根据两个相邻的路口获取其间的roadId,不考虑方向
        :param crossId1: int
        :param crossId2: int
        :return:
        """
        crossIdList = [crossId1, crossId2]
        roadIdList = self.roads.getRoadIdList()
        for roadId in roadIdList:
            if (self.roads.getRoadFromCrossByRoadId(roadId) in crossIdList) \
                    and (self.roads.getRoadToCrossByRoadId(roadId) in crossIdList):
                return roadId
        return None

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
        head_width = 6 * width  # 3
        head_length = 2.5 * head_width  # 1.5
        if (crossId is None or roadId is None) \
                or (self.roads.getRoadFromCrossByRoadId(roadId) is crossId or self.roads.isDuplexByRoadId(roadId)):
            plt.arrow(x, y, newX - x, newY - y, color='r', width=width, head_width=head_width, head_length=head_length,
                      length_includes_head=True)

    def showRoadIdAndLengthFunc(self, x, y, roadId, roadLength, showRoadId):
        if showRoadId is True:
            plt.text(x, y,
                     str(roadId) + '(' + str(roadLength) + ')',
                     fontdict=self.font1)

    def __dfs(self, x, y, crossId, showRoadId):
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
                  self.roads.getAnotherCrossIdByRoadId(crossId, upRoadId))
            # plt.text((newX + x) / 2, (newY + y) / 2,
            #          str(upRoadId) + '(' + str(self.roads.getRoadLengthByRoadId(upRoadId)) + ')',
            #          fontdict=self.font1)
            self.showRoadIdAndLengthFunc((newX + x) / 2, (newY + y) / 2, upRoadId,
                                         self.roads.getRoadLengthByRoadId(upRoadId), showRoadId)
            self.__dfs(newX, newY, self.roads.getAnotherCrossIdByRoadId(crossId, upRoadId), showRoadId)
        if rightRoadId != -1:
            newX = x + self.interval
            newY = y
            self.addArrow(crossId, rightRoadId, x, y, newX, newY)
            # plt.text((newX + x) / 2, (newY + y) / 2,
            #          str(rightRoadId) + '(' + str(self.roads.getRoadLengthByRoadId(rightRoadId)) + ')',
            #          fontdict=self.font1)
            self.showRoadIdAndLengthFunc((newX + x) / 2, (newY + y) / 2, rightRoadId,
                                         self.roads.getRoadLengthByRoadId(rightRoadId), showRoadId)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.roads.getAnotherCrossIdByRoadId(crossId, rightRoadId))
            self.__dfs(newX, newY, self.roads.getAnotherCrossIdByRoadId(crossId, rightRoadId), showRoadId)
        if downRoadId != -1:
            newX = x
            newY = y - self.interval
            self.addArrow(crossId, downRoadId, x, y, newX, newY)
            # plt.text((newX + x) / 2, (newY + y) / 2,
            #          str(downRoadId) + '(' + str(self.roads.getRoadLengthByRoadId(downRoadId)) + ')',
            #          fontdict=self.font1)
            self.showRoadIdAndLengthFunc((newX + x) / 2, (newY + y) / 2, downRoadId,
                                         self.roads.getRoadLengthByRoadId(downRoadId), showRoadId)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.roads.getAnotherCrossIdByRoadId(crossId, downRoadId))
            self.__dfs(newX, newY, self.roads.getAnotherCrossIdByRoadId(crossId, downRoadId), showRoadId)
        if leftRoadId != -1:
            newX = x - self.interval
            newY = y
            self.addArrow(crossId, leftRoadId, x, y, newX, newY)
            # plt.text((newX + x) / 2, (newY + y) / 2,
            #          str(leftRoadId) + '(' + str(self.roads.getRoadLengthByRoadId(leftRoadId)) + ')',
            #          fontdict=self.font1)
            self.showRoadIdAndLengthFunc((newX + x) / 2, (newY + y) / 2, leftRoadId,
                                         self.roads.getRoadLengthByRoadId(leftRoadId), showRoadId)
            print('x=', x, 'y=', y, 'oldCrossId=', crossId, 'newCrossId=',
                  self.roads.getAnotherCrossIdByRoadId(crossId, leftRoadId))
            self.__dfs(newX, newY, self.roads.getAnotherCrossIdByRoadId(crossId, leftRoadId), showRoadId)

    def plotMap(self, showRoadId=True):
        """
        绘制地图，由于路段长短弯直不一，无法精确绘制。
        绘制各点距离暂定为self.interval.在自带的10张地图没有出现问题。
        :param showRoadId: 决定是否显示RoadId
        :return:
        """
        self.__dfs(0, 0, self.crosses.getCrossIdList()[0], showRoadId)
        plt.show()

    def initialDirGraph(self, crossRelation, roadInstances):
        """
        使用networkx初始化有向图，使用fqy的crossRelation和roadInstances结构
        :param crossRelation:
        :param roadInstances:
        :return:
        """
        G = nx.DiGraph()
        for i in crossRelation.keys():
            for j in crossRelation[i].keys():
                G.add_weighted_edges_from([(i, j, roadInstances[crossRelation[i][j]].length)])
        nx.draw_networkx(G, with_labels=True, arrows=True)
        self.graph = G

    def getDirGraph(self):
        return self.graph


if __name__ == "__main__":
    configPath = "../CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    mapHelperVar = MapHelper(dataCross, dataRoad)
    # print(mapHelperVar.crosses.getCrossIdList())
    # print(mapHelperVar.crosses.getCrossIdList()[10])
    # print(mapHelperVar.getRoadIdByDirection(10, 'up')
    #       , mapHelperVar.getRoadIdByDirection(10, 'right')
    #       , mapHelperVar.getRoadIdByDirection(10, 'down')
    #       , mapHelperVar.getRoadIdByDirection(10, 'left'))
    # plt.subplot(121)
    mapHelperVar.plotMap(showRoadId=True)
    # plt.subplot(122)
    trafficMap = Map(configPath)
    mapHelperVar.initialDirGraph(trafficMap.crossRelation, generateRoadInstances(configPath))
    # plt.show()
    crossesIdList = nx.shortest_path(mapHelperVar.getDirGraph(), source='1', target='36', weight='weight')
    # print(crossesIdList)
    roadIdList = list()
    for index in range(1, len(crossesIdList)):
        roadIdList.append(mapHelperVar.getRoadIdByTwoCrossIds(int(crossesIdList[index - 1]), int(crossesIdList[index])))
    print(roadIdList)
