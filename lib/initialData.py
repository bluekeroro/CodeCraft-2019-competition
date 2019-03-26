# -*- coding:UTF-8 -*-
"""
@File    : initialData.py
@Time    : 2019/3/10 19:26
@Author  : Blue Keroro
"""


def initial(carTxtPath, crossTxtPath, roadTxtPath):
    """
    将txt数据转为csv,以便于使用pandas读取
    :param configPath: txt数据文件路径
    :return:
    """
    rawPathList = [carTxtPath, crossTxtPath, roadTxtPath]
    for path in rawPathList:
        CSVPath = changeTXTpathToCSV(path)
        with open(CSVPath, 'w') as f, open(path, 'r') as f1:
            for line in f1:
                line = line.replace("#", '')
                line = line.replace("(", '')
                line = line.replace(")", '')
                f.write(line)


def changeTXTpathToCSV(path):
    """
    將txt文件路徑換位為相同的csv文件路徑
    :param path:
    :return:
    """
    return path[:-3] + 'csv'


if __name__ == "__main__":
    carTxtPath = "../config/car.txt"
    crossTxtPath = "../config/cross.txt"
    roadTxtPath = "../config/road.txt"
    initial(carTxtPath, crossTxtPath, roadTxtPath)
