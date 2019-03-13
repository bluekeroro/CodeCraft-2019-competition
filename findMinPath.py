import pandas as pd
from lib import initialData
from lib.cross import Cross
from lib.cross import Crosses
from lib import mapHelper
from lib.road import Roades
from lib.road import Road

direct = ["up", "right", "down", "left"]


def findMinPath(map, crosses, roads):
    """
    根据地图获取地图上每个路口到其余路口的最短路径
    两次遍历所有点，求各点之间最短路径
    :param map:
    :return:
    """
    for crossid1 in crosses.getCrossIdList() :
        for crossid2 in crosses.getCrossIdList():
            flag = [0] * (len(crosses.getCrossIdList()) + 1)
            flag[crossid1] = 1
            min = [1000] #当前最小距离 使用min[0]调用
            ret = []
            temp = []
            if crossid1 == crossid2:
                continue
            else:
                helper(crossid1, crossid2, map, ret, temp, roads, flag, 0,min)
        print(str(crossid1) + "to" + str(crossid2) + ":")
        print(ret)


def helper(crossid1, crossid2, map, ret, temp,roads,flag,cur,min):
    """
    回溯算法的辅助函数, 从crossid1出发至crossId2 找一条路
    :param crossId1,出发点
           crossId2,终点
           map, maphelper对象
           ret, 存储最短路径
           temp，存储路径
           roads，roads对象
           flag，记录当前点是否被走过
           cur, 当前距离
           min, 当前最小距离
    :return:
    """
    if(crossid1 == crossid2 & cur < min[0]):
        t = temp
        min[0] = cur
        ret.pop() # 清空ret
        ret.append(t)
        return
    for dir in direct:
        newRoadId = map.getRoadIdByDirection(crossid1,dir)
        if newRoadId != -1:
            newCrossId = roads.getAnotherCrossIdByRoadId(crossid1, newRoadId)
            if flag[newCrossId] == 0:
                 temp.append(newRoadId)
                 flag[newCrossId] = 1
                 cur += roads.getRoadLengthByRoadId(newRoadId)
                 if cur > min[0] : break  # 当前距离超过当前最小值，剪枝
                 helper(newCrossId,crossid2,map,ret,temp,roads,flag,cur,min)
                 temp.pop()
                 flag[newCrossId] = 0
            else : continue
        else : continue
    return


if __name__ == '__main__':
    configPath = "CodeCraft-2019/config_10"
    initialData.initial(configPath)
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    mapHelperVar = mapHelper.MapHelper(dataCross, dataRoad)
    crossesVar = Crosses(dataCross)
    roadsVar = Roades(dataRoad)
    findMinPath(mapHelperVar, crossesVar, roadsVar)