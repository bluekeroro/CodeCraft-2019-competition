# -*- coding:UTF-8 -*-

from lib.myLogger import MyLogger


class Map(object):
    def __init__(self, configCrossPath, configRoadPath):
        self.configCrossPath = configCrossPath
        self.configRoadPath = configRoadPath
        self.crossData = {} # 路口数据
        self.roadData = {} # 道路数据
        self.crossRelation = {} # 路口的连接关系
        self.roadRelation = {} # 道路的连接关系

        self.__build()

    def __build(self):
        """
        建立路口和道路的连接关系
        """
        with open(self.configCrossPath, 'r') as crossFile, open(self.configRoadPath, 'r') as roadFile:
            crossFile.readline() # 跳过第一行
            roadFile.readline() # 跳过第一行
            for line in crossFile:
                line = line.replace('(', '').replace(')', '').replace('\n', '')
                line = line.split(', ')
                self.crossData[line[0]] = line
            for line in roadFile:
                line = line.replace('(', '').replace(')', '').replace('\n', '')
                line = line.split(', ')
                self.roadData[line[0]] = line

        # 生成路口连接关系
        self.crossRelation = {cross[0]:{} for cross in self.crossData.values()}
        for road in self.roadData.values():
            roadId = road[0]
            src = road[4]
            dst = road[5]
            self.crossRelation[src][dst] = roadId + '-1'
            if int(road[6]):
                self.crossRelation[dst][src] = roadId + '-2'

        # 生成道路转向关系
        for i in self.crossRelation:
            for j in self.crossRelation[i]:
                srcRoad = self.crossRelation[i][j]
                r4 = self.crossData[j][1:]
                srcDirNum = r4.index(srcRoad[:-2])
                self.roadRelation[srcRoad] = {}
                for dstRoad in self.crossRelation[j].values():
                    if dstRoad[:-2] == srcRoad[:-2]:
                        pass
                    else:
                        dstDirNum = r4.index(dstRoad[:-2])
                        dirValue = dstDirNum - srcDirNum
                        if dirValue == 2 or dirValue == -2:
                            self.roadRelation[srcRoad][dstRoad] = 'forward'
                        if dirValue == 1 or dirValue == -3:
                            self.roadRelation[srcRoad][dstRoad] = 'left'
                        if dirValue == -1 or dirValue == 3:
                            self.roadRelation[srcRoad][dstRoad] = 'right'

    def getNeighborCross(self, crossId):
        """
        获取可达的下一个路口
        """
        if crossId in self.crossRelation:
            return self.crossRelation[crossId]
        else:
            raise Exception("Cross Id Not Exist")

    def getNeighborRoad(self, roadId):
        """
        获取可达的下一个道路
        """
        if roadId in self.roadRelation:
            return self.roadRelation[roadId]
        else:
            raise Exception("Road Id Not Exist")
        

if __name__ == '__main__':
    configCrossPath = '../config/cross.txt'
    configRoadPath = '../config/road.txt'
    trafficMap = Map(configCrossPath, configRoadPath)
    MyLogger.print(trafficMap.crossRelation)
    MyLogger.print(trafficMap.roadRelation)
