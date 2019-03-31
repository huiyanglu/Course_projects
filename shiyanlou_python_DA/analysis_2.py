#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

"""
Created date: 2019-03-31

Introduction:
使用 Pandas 读取 json 文件，并从中统计出第二个参数指定的用户 ID 的学习次数和总学习分钟数，
也就是说函数将返回两个值，第一个为指定用户的学习时间，第二个为指定用户的总学习分钟数。

"""

import json
import pandas as pd

def analysis(file,user_id):
    times = 0
    minutes = 0

    try:
        f = pd.read_json(file)
    except:
        return 0

    if f[f['user_id'] == user_id].empty:
        return 0
    else:
        #布尔索引筛选出所有相关行
        df = f[f['user_id'] == user_id]
        times = df.shape[0] #学习次数
        minutes = df['minutes'].sum() #总分钟数

    return times,minutes

print(analysis('user_study.json',199071))