# -*- coding:utf-8 -*-
import sys
import os

from lib.initialData import changeTXTpathToCSV

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import logging
import pandas as pd
import datetime
from lib import initialData
from lib.car import Cars, Car
from lib.mapHelper import MapHelper
from lib_fqy.map import Map
from lib_fqy.road import generateRoadInstances

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    starttime = datetime.datetime.now()
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)
    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]
    configPath = ''
    for i in range(len(car_path) - 1, -1, -1):
        if car_path[i] == '/':
            configPath = car_path[0:i]

    print(car_path, road_path, cross_path, answer_path)
    print(configPath)

    # car_path = '../config/car.txt'
    # road_path = '../config/road.txt'
    # cross_path = '../config/cross.txt'
    # answer_path = '../config/answer.txt'
    #
    # configPath = '../config'
    initialData.initial(car_path, cross_path, road_path)
    dataCross = pd.read_csv(changeTXTpathToCSV(cross_path))
    dataRoad = pd.read_csv(changeTXTpathToCSV(road_path))
    dataCar = pd.read_csv(changeTXTpathToCSV(car_path))
    mapHelperVar = MapHelper(dataCross, dataRoad)
    trafficMap = Map(configPath, cross_path, road_path)
    roadInstances = generateRoadInstances(road_path)
    mapHelperVar.initialDirGraph(trafficMap.crossRelation, roadInstances)
    carDict = {}
    carVar = Cars(dataCar)
    file = open(answer_path, 'w')
    path = {}
    for carId in carVar.getCarIdList():
        carDict[carId] = Car(carId, carVar)
        fromCrossId = str(carDict[carId].getCarFrom())
        toCrossId = str(carDict[carId].getCarTo())
        if fromCrossId not in path:
            print("fromCrossId=", fromCrossId)
            path.update(
                mapHelperVar.findAllShortestPathByMyDijkstra(fromCrossId, trafficMap.crossRelation, roadInstances))
        print(carId)
        carDict[carId].addDrivePath(path[fromCrossId][toCrossId])
        string = str((carId, carDict[carId].getCarPlanTime(), carDict[carId].getDrivePath()))
        string = string.replace('[', '')
        string = string.replace(']', '')
        file.write(string + '\n')
    file.close()
    endtime = datetime.datetime.now()
    print('运行时间:', (endtime - starttime).total_seconds())  # 运行时间:  58.1495s


# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
