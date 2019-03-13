# -*- coding:UTF-8 -*-
"""
@File    : main.py
@Time    : 2019/3/10 18:20
@Author  : Blue Keroro
"""
import pandas as pd
import logging
import os
from lib import initialData

logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.dirname(os.path.abspath(__file__)) + '/logs/CodeCraft-2019.log',
                    filemode='a',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    configPath = 'CodeCraft-2019/config'
    initialData.initial(configPath)
    dataCar = pd.read_csv(configPath + '/car.csv')
    dataCross = pd.read_csv(configPath + '/cross.csv')
    dataRoad = pd.read_csv(configPath + '/road.csv')
    print(dataCar.head(5))
    print(dataCross.head(5))
    print(dataRoad.head(5))
    print("start")


if __name__ == "__main__":
    main()
