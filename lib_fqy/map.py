# -*- coding:UTF-8 -*-

import pandas as pd


class Map(object):
    def __init__(self, configPath):
        self.configPath = configPath
        self.crossRelation = {} # 路口的连接关系
        self.roadRelation = {} # 道路的连接关系

        self.__build()

    def __build(self):
        """
        建立路口和道路的连接关系
        """
        crossData = pd.read_csv(self.configPath + '/cross.csv')
        roadData = pd.read_csv(self.configPath + '/road.csv')

        self.crossRelation = {str(i):{} for i in crossData['id']}
        for index, row in roadData.iterrows():
            roadId = str(row['id'])
            src = str(row['from'])
            dst = str(row['to'])
            self.crossRelation[src][dst]=roadId+'-1'
            if row['isDuplex']:
                self.crossRelation[dst][src]=roadId+'-2'

        for i in self.crossRelation:
            for j in self.crossRelation[i]:
                srcRoad = self.crossRelation[i][j]
                r4 = crossData[crossData['id']==int(j)].iloc[0]
                r4 = (str(r4['roadId']),str(r4['roadId.1']),str(r4['roadId.2']),str(r4['roadId.3']))
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
    configPath = '../CodeCraft-2019/config_10'
    trafficMap = Map(configPath)
    print(trafficMap.crossRelation)
    print(trafficMap.roadRelation)

