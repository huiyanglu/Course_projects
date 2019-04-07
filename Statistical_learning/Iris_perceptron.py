#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
"""
第2章 感知机
二分类模型
𝑓(𝑥)=𝑠𝑖𝑔𝑛(𝑤∗𝑥+𝑏)
损失函数 𝐿(𝑤,𝑏)=−Σ𝑦𝑖(𝑤∗𝑥𝑖+𝑏)

算法
随即梯度下降法 Stochastic Gradient Descent
随机抽取一个误分类点使其梯度下降。

当实例点被误分类，即位于分离超平面的错误侧，则调整w, b的值，
使分离超平面向该无分类点的一侧移动，直至误分类点被正确分类

拿出iris数据集中两个分类的数据和[sepal length，sepal width]作为特征
"""
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris #导入IRIS数据集
import matplotlib.pyplot as plt

# load data
iris = load_iris() #特征矩阵
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['label'] = iris.target #iris.target为目标值


# 设置所有列标签
df.columns = ['sepal length', 'sepal width', 'petal length', 'petal width', 'label']
print(df.label.value_counts()) #label列统计每个数字出现的次数

"""
生成一幅散点图

# 画label为0的50个散点
plt.scatter(df[:50]['sepal length'], df[:50]['sepal width'], label='0')
# 画label为1的50个散点
plt.scatter(df[50:100]['sepal length'], df[50:100]['sepal width'], label='1')
plt.xlabel('sepal length') # x轴
plt.ylabel('sepal width') # y轴
plt.legend() # 图例
#plt.show()
"""
data = np.array(df.iloc[:100, [0, 1, -1]]) #前100行，第1、2列和最后一列
X, y = data[:,:-1], data[:,-1] # X为第1、2列，y为最后一列
y = np.array([1 if i == 1 else -1 for i in y])


# 数据线性可分，二分类数据
# 此处为一元一次线性方程
class Model:
    def __init__(self):
        self.w = np.ones(len(data[0]) - 1, dtype=np.float32)
        self.b = 0
        self.l_rate = 0.1 #步长（大于等于0，小于等于1）
        # self.data = data

    def sign(self, x, w, b): # w.x+b（点乘）
        y = np.dot(x, w) + b
        return y

    # 随机梯度下降法
    def fit(self, X_train, y_train): #X是点的横纵坐标数组，y为1或-1判断在平面的左右位置
        is_wrong = False
        while not is_wrong:
            wrong_count = 0 #误分类个数
            for d in range(len(X_train)): #遍历每个点
                X = X_train[d]
                y = y_train[d]
                if y * self.sign(X, self.w, self.b) <= 0: #如果<=0则该点误分类
                    self.w = self.w + self.l_rate * np.dot(y, X)
                    self.b = self.b + self.l_rate * y
                    wrong_count += 1
            if wrong_count == 0:
                is_wrong = True
        return 'Perceptron Model!'

    def score(self):
        pass


perceptron = Model()
perceptron.fit(X, y)

x_points = np.linspace(4, 7,10) #在4-7之间固定距离取10个数
print(x_points)
y_ = -(perceptron.w[0]*x_points + perceptron.b)/perceptron.w[1] #求纵坐标
plt.plot(x_points, y_) #生成一条直线

plt.plot(data[:50, 0], data[:50, 1], 'bo', color='blue', label='0')
plt.plot(data[50:100, 0], data[50:100, 1], 'bo', color='orange', label='1')
plt.xlabel('sepal length')
plt.ylabel('sepal width')
plt.legend()
#plt.show()

from sklearn.linear_model import Perceptron

clf = Perceptron(fit_intercept=False, max_iter=1000, shuffle=False)
clf.fit(X, y)
# Weights assigned to the features.
print(clf.coef_)
# 截距 Constants in decision function.
print(clf.intercept_)

x_ponits = np.arange(4, 8)
y_ = -(clf.coef_[0][0]*x_ponits + clf.intercept_)/clf.coef_[0][1]
plt.plot(x_ponits, y_)

plt.plot(data[:50, 0], data[:50, 1], 'bo', color='blue', label='0')
plt.plot(data[50:100, 0], data[50:100, 1], 'bo', color='orange', label='1')
plt.xlabel('sepal length')
plt.ylabel('sepal width')
plt.legend()
plt.show()
