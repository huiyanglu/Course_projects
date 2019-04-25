#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
"""
根据爬虫获取的数据文件进行数据分析
"""

import numpy
import matplotlib.pyplot as plt

price,size = numpy.loadtxt('house.csv',delimiter='|',usecols=(1,2),unpack=True)

print(price,size)

price_mean = numpy.mean(price)
size_mean = numpy.mean(size)

print('价格的均值为：',price_mean)
print('面积的均值为：',size_mean)

price_var = numpy.var(price)
size_var = numpy.var(size)

print('价格的方差为：',price_var)
print('面积的方差为：',size_var)

price_per_size = [price[i]/size[i] for i in range(len(price))]
rst = [i for i in price_per_size if i<20]
print(rst)

plt.figure()
plt.subplot(211)
#plt.title("price")
plt.title("Price / 10000RMB")
plt.hist(price, bins=20)

plt.subplot(212)
#plt.title("area")
plt.xlabel("Size / m**2")
plt.hist(size, bins=20)

plt.figure(2)
plt.title("Price/size")
plt.plot(rst)

plt.show()

