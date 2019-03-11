# -*- coding:UTF-8 -*-
"""
@File    : myLog.py
@Time    : 2019/3/10 18:42
@Author  : Blue Keroro
"""
import logging
import os


class myLog(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            filename=os.path.dirname(os.path.abspath(__file__)) + '/logs/CodeCraft-2019.log',
                            filemode='a',
                            format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    def info(self, msg, *args, **kwargs):
        logging.info(msg, *args, **kwargs)
        print(*args)
        print(msg)


if __name__ == '__main__':
    myLog().info("test")
    print("finish")
