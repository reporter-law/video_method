"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from sys import path
path.append(r'J:\PyCharm项目\学习书籍成果\其他库\语音播报\天气查询程序')
from WeatherAPITest import weather_main as wm

#print(wm("长沙"))
a = "长沙长沙长沙郴州"
a1 = list(a)
print(a1)
fre = {}
for i in a1:
    if i in fre:
        fre[i] += 1
    else:
        fre[i] =1
print(fre)
for number,i in enumerate(fre.values()):
    if i >1:
        pass
    else:
        print(list(fre.keys())[number])




for i in [('长沙镇', 90), ('长沙乡', 90), ('长沙乡', 90), ('长沙市', 90), ('长沙雨花经济开发区管理委员会', 90)]:
    if "市" in i[0]:
        print(i)