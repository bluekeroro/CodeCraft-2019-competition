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
    if len(sys.argv) == 5:
        MyLogger.setEnable(False)
        car_path = sys.argv[1]
        road_path = sys.argv[2]
        cross_path = sys.argv[3]
        answer_path = sys.argv[4]
    else:
        car_path = '../config/car.txt'
        road_path = '../config/road.txt'
        cross_path = '../config/cross.txt'
        answer_path = '../config/answer.txt'

    # configPath = ''
    # for i in range(len(car_path) - 1, -1, -1):
    #     if car_path[i] == '/':
    #         configPath = car_path[0:i]
    # MyLogger.print(car_path, road_path, cross_path, answer_path)
    # MyLogger.print(configPath)

    initialData.initial(car_path, cross_path, road_path)
    dataCar = pd.read_csv(changeTXTpathToCSV(car_path))
    dataCar['DriveDistance'] = None
    mapHelperVar = MapHelper()
    trafficMap = Map(cross_path, road_path)
    roadInstances = generateRoadInstances(road_path)
    # mapHelperVar.initialDirGraph(trafficMap.crossRelation, roadInstances)
    carDict = {}
    file = open(answer_path, 'w')
    print("初始化时间：", (datetime.datetime.now() - starttime).total_seconds())
    path = getShortestPath(trafficMap, roadInstances)
    for carId in Cars.getCarIdList():
        MyLogger.print(carId)
        fromCrossId = str(Cars.getCarFromByCarId(carId))
        toCrossId = str(Cars.getCarToByCarId(carId))
        # carDict[carId] = Car(carId)
        # fromCrossId = str(carDict[carId].getCarFrom())
        # toCrossId = str(carDict[carId].getCarTo())
        pathRoadIdIntList = list()
        for i in path[fromCrossId][toCrossId]['path']:
            pathRoadIdIntList.append(int(i.split('-')[0]))
        # carDict[carId].addDrivePath(pathRoadIdIntList)
        # carDict[carId].setDriveDistance(path[fromCrossId][toCrossId]['length'])
        carDict[carId] = pathRoadIdIntList
        dataCar.loc[dataCar['id'] == carId, 'DriveDistance'] = path[fromCrossId][toCrossId]['length']
    dataCar = dataCar.sort_values(by=['speed', 'DriveDistance'], ascending=[False, True])
    count = 10
    print("规划时间：", (datetime.datetime.now() - starttime).total_seconds())
    for index, row in dataCar.iterrows():
        # string = str((row['id'], count, carDict[row['id']].getDrivePath()))
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
