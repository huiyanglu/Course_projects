#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
"""
Created date: 2019-03-29

Introduction:
在函数中解析 json 文件
从中统计出第二个参数指定的用户 ID 的学习次数和总学习分钟数
即函数将返回两个值
第一个为指定用户的学习次数
第二个为指定用户的总学习分钟数。
"""

import json

def analysis(file, user_id):
    times = 0
    minutes = 0

    with open(file,'r') as f:
        load_d = json.load(f) #加载打开的json文件
        print(load_d[0])

    for data in load_d:
        #刚开始没有加这个for循环，报错了，如图所示
        uid = data['user_id']
        u_minutes = data['minutes']
        if uid == user_id: #判断，找需要的数字
            times += 1
            minutes += u_minutes
    return times, minutes

if __name__ == '__main__':
    a =analysis('user_study.json', 199071)
    print(a)