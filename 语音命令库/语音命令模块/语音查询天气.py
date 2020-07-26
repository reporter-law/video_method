"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import re
from sys import path
path.append(r'J:\PyCharm项目\学习书籍成果\其他库\语音播报\天气查询程序')
from WeatherAPITest import weather_main as wm
from 语音命令库.语音命令模块.语音命令模块 import command_speak as cs
from jieba import posseg as psg
from fuzzywuzzy import process


command = cs()
for command in command:
    print(command)

    city = []
    city_ = []
    for x in psg.lcut(command.strip()):
        if x.flag in ['n', 'nr', 'ns'] and len(x.word) > 1:
            city.append(x.word)
    print(city)
    for city in city:
        with open(r"E:\360Downloads\AreaCity-JsSpider-StatsGov-master\src\采集到的数据\Step1_1_StatsGov.txt", "r",
                  encoding="utf-8")as f:
            a = f.read()
            content = re.findall(r'[\u4e00-\u9fa5]+', a)
            content = process.extract(city, content)
            for i in content:
                if i[1] >= 90:
                    wm(city)
                    break
