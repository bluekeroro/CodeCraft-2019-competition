# -*- coding:UTF-8 -*-
"""
@File    : initialData.py
@Time    : 2019/3/10 19:26
@Author  : Blue Keroro
"""
import pandas as pd

def initial(carTxtPath, crossTxtPath, roadTxtPath):
    """
    将txt数据转为csv,以便于使用pandas读取
    :param configPath: txt数据文件路径
    :return:
    """
    # configPath = "CodeCraft-2019/config"
    carPath = carTxtPath
    crossPath = crossTxtPath
    roadPath = roadTxtPath
    carCSVPath = changeTXTpathToCSV(carTxtPath)
    crossCSVPath = changeTXTpathToCSV(crossTxtPath)
    roadCSVPath = changeTXTpathToCSV(roadTxtPath)
    try:
        f = open(carPath, 'r')
        f1 = open(carCSVPath, 'w')
        for line in f.readlines():
            line = line.replace("#", '')
            line = line.replace("(", '')
            line = line.replace(")", '')
            f1.write(line)
    finally:
        if f:
            f.close()
        if f1:
            f1.close()
    try:
        f = open(crossPath, 'r')
        f1 = open(crossCSVPath, 'w')
        for line in f.readlines():
            line = line.replace("#", '')
            line = line.replace("(", '')
            line = line.replace(")", '')
            f1.write(line)
    finally:
        if f:
            f.close()
        if f1:
            f1.close()
    try:
        f = open(roadPath, 'r')
        f1 = open(roadCSVPath, 'w')
        for line in f.readlines():
            line = line.replace("#", '')
            line = line.replace("(", '')
            line = line.replace(")", '')
            f1.write(line)
    finally:
        if f:
            f.close()
        if f1:
            f1.close()


def changeTXTpathToCSV(path):
    """
    將txt文件路徑換位為相同的csv文件路徑
    :param path:
    :return:
    """
    return path[:-3]+'csv'


if __name__ == "__main__":
    configPath = "../config"
    carTxtPath = "../config/car.txt"
    crossTxtPath = "../config/cross.txt"
    roadTxtPath = "../config/road.txt"
    initial(carTxtPath, crossTxtPath, roadTxtPath)
    dataCar = pd.read_csv(configPath + '/car.csv')
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    print(dataCar.head(5))
    print(dataCross.head(5))
    print(dataRoad.head(5))
