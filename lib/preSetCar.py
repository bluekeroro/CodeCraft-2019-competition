# -*- coding:UTF-8 -*-
"""
@File    : preSetCar.py
@Time    : 2019/4/1 10:12
@Author  : Blue Keroro
"""
import pandas as pd

from lib.myLogger import MyLogger


class PreSetCar(object):
    def __init__(self, **data):
        self.id = data['id']  # 车的id
        self.time = data['time']  # 车的出发时间
        self.route = data['route']  # 车的预置路线


def generatePreSetCarInstances(configPath):
    """
    生成预置车辆的实例
    """
    carSet = {}
    carData = pd.read_csv(configPath)
    for index, row in carData.iterrows():
        data = {
            'id': str(row['carid']),
            'time': str(row['time']),
            'route': eval(row['roadId1...'])
        }
        carSet[data['id']] = PreSetCar(**data)

    return carSet


if __name__ == '__main__':
    presetAnswer_path = '../config/presetAnswer.csv'
    cars = generatePreSetCarInstances(presetAnswer_path)
    MyLogger.print(cars['21701'].__dict__)
