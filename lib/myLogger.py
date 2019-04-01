# -*- coding:UTF-8 -*-
"""
@File    : myLogger.py
@Time    : 2019/3/21 14:49
@Author  : Blue Keroro
"""


class MyLogger(object):
    """
    创建统一的打印方法
    因为最后提交时如果含有print方法可能会引起运行失败
    """
    enable = True

    @classmethod
    def print(cls, *args):
        if cls.enable:
            print(*args)

    @classmethod
    def setEnable(cls, enable):
        cls.enable = enable

    @classmethod
    def getEnable(cls):
        return cls.enable


if __name__ == "__main__":
    MyLogger.print("hhhh", "jkklll1")
    MyLogger.setEnable(False)
    MyLogger.print("hhhh", "jkklll2")
    MyLogger.setEnable(True)
    MyLogger.print("hhhh", "jkklll3")
