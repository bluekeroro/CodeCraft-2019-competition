import logging
import sys

import pandas as pd
import datetime
from lib import initialData
from lib.car import Cars, Car
from lib.mapHelper import MapHelper
from lib_fqy.map import Map
from lib_fqy.road import generateRoadInstances

logging.basicConfig(level=logging.DEBUG,
                    filename='./../logs/CodeCraft-2019.log',
                    # filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    starttime = datetime.datetime.now()
    # if len(sys.argv) != 5:
    #     logging.info('please input args: car_path, road_path, cross_path, answerPath')
    #     exit(1)
    # car_path = sys.argv[1]
    # road_path = sys.argv[2]
    # cross_path = sys.argv[3]
    # answer_path = sys.argv[4]
    car_path = '../config/car.txt'
    road_path = '../config/road.txt'
    cross_path = '../config/cross.txt'
    answer_path = '../config/answer.txt'

    configPath = '../config'
    initialData.initial(configPath)
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    dataCar = pd.read_csv(configPath + '/car.csv')
    mapHelperVar = MapHelper(dataCross, dataRoad)
    trafficMap = Map(configPath)
    roadInstances = generateRoadInstances(configPath)
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
            path[fromCrossId] = {}
        if toCrossId not in path[fromCrossId]:
            print(fromCrossId, toCrossId)
            # pathTemp = mapHelperVar \
            #     .findShortestPathByMyDijkstra(fromCrossId, toCrossId, trafficMap.crossRelation, roadInstances)
            pathTemp = mapHelperVar.findShortPathByTSY(fromCrossId, toCrossId)
            path[fromCrossId][toCrossId] = pathTemp
        print(carId)
        carDict[carId].addDrivePath(path[fromCrossId][toCrossId])
        string = str((carId, carDict[carId].getCarPlanTime(), carDict[carId].getDrivePath()))
        string = string.replace('[', '')
        string = string.replace(']', '')
        file.write(string + '\n')
    file.close()
    endtime = datetime.datetime.now()
    print('运行时间:', (endtime - starttime).total_seconds())  # 运行时间: 1451.860217


# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
