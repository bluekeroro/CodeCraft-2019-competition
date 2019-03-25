# -*- coding:utf-8 -*-
import sys
import os

from lib_fqy.shortestpath import getShortestPath

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from lib.myLogger import MyLogger
from lib.initialData import changeTXTpathToCSV
import logging
import pandas as pd
import datetime
from lib import initialData
from lib.car import Cars, Car
from lib.mapHelper import MapHelper
from lib_fqy.map import Map
from lib_fqy.road import generateRoadInstances


def planTimeWeighted(car):
    """
    对计划时间加权
    :param car:
    :return: int
    """
    planTime = car.getCarPlanTime()
    speed = car.getCarLargestSpeed()
    planTimeMin = Cars.getCarPlanTimeMin()
    planTimeMax = Cars.getCarPlanTimeMax()
    speedMin = Cars.getCarSpeedMin()
    speedMax = Cars.getCarSpeedMax()
    temp = int((speedMax - speed) / speedMax * 500)
    if temp > planTime:
        planTime = temp
    return planTime


def main():
    starttime = datetime.datetime.now()
    if len(sys.argv) == 5: # 如果运行时没有输入参数，则将路径设为默认路径
        MyLogger.setEnable(False) # 如果输入参数了，则说明提交到了平台，需要关闭打印
        car_path = sys.argv[1]
        road_path = sys.argv[2]
        cross_path = sys.argv[3]
        answer_path = sys.argv[4]
    else:
        car_path = '../config/car.txt'
        road_path = '../config/road.txt'
        cross_path = '../config/cross.txt'
        answer_path = '../config/answer.txt'

    initialData.initial(car_path, cross_path, road_path) # 初始化，将txt转为csv
    dataCar = pd.read_csv(changeTXTpathToCSV(car_path)) # 读取csv存为dataframe以便后续不同的策略排序
    dataCar['DriveDistance'] = None # 策略排序需要考虑的因素
    trafficMap = Map(cross_path, road_path)
    roadInstances = generateRoadInstances(road_path)
    carDict = {}
    file = open(answer_path, 'w') # 到这里耗时1s左右
    print("初始化时间：", (datetime.datetime.now() - starttime).total_seconds())
    path = getShortestPath(trafficMap, roadInstances)
    for carId in Cars.getCarIdList(): # 对全部车辆的遍历，将距离写入dataCar中，对路径截断
        MyLogger.print(carId)
        fromCrossId = str(Cars.getCarFromByCarId(carId))
        toCrossId = str(Cars.getCarToByCarId(carId))
        pathRoadIdIntList = list()
        for i in path[fromCrossId][toCrossId]['path']: # 对路径截断
            pathRoadIdIntList.append(int(i.split('-')[0]))
        carDict[carId] = pathRoadIdIntList # 将截断的路径存入字典中
        dataCar.loc[dataCar['id'] == carId, 'DriveDistance'] = path[fromCrossId][toCrossId]['length']
    dataCar = dataCar.sort_values(by=['speed', 'DriveDistance'], ascending=[False, True]) # 速度从大到小排，然后行驶距离从小到大排
    count = 10 # plantime时间，从10开始，一次累加，不适合后续大地图
    print("规划时间：", (datetime.datetime.now() - starttime).total_seconds())
    for index, row in dataCar.iterrows(): # 将data写入answer中
        string = str((row['id'], count, carDict[row['id']]))
        string = string.replace('[', '')
        string = string.replace(']', '')
        file.write(string + '\n')
        count += 1
    file.close()
    endtime = datetime.datetime.now()
    MyLogger.print('运行时间:', (endtime - starttime).total_seconds())  # 运行时间:  58.1495s


# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
