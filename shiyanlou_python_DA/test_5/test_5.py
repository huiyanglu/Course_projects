#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

import pandas as pd

data = pd.read_csv('apple.csv', header=0)

# 将Date列转换为时间索引
i = pd.to_datetime(data['Date'])

#读取Volume列数据并添加日期索引
data_Volume = pd.Series(data['Volume'].values,index=i)

#按季度重采样
data_Q = data_Volume.resample('Q').sum()

#按照volume列的大小排序 返回第二项数据 ascending决定升降序
second_volume = data_Q.sort_values(ascending=False)[1]

print(second_volume)