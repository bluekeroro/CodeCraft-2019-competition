# -*- coding:UTF-8 -*-
"""
@File    : initialData.py
@Time    : 2019/3/10 19:26
@Author  : Blue Keroro
"""
import pandas as pd


def initial(configPath):
    # configPath = "CodeCraft-2019/config"
    carPath = configPath + "/car.txt"
    crossPath = configPath + "/cross.txt"
    roadPath = configPath + "/road.txt"
    carCSVPath = configPath + "/car.csv"
    crossCSVPath = configPath + "/cross.csv"
    roadCSVPath = configPath + "/road.csv"
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


if __name__ == "__main__":
    configPath = "CodeCraft-2019/config"
    initial(configPath)
    dataCar = pd.read_csv(configPath + '/car.csv')
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    print(dataCar.head(5))
    print(dataCross.head(5))
    print(dataRoad.head(5))
