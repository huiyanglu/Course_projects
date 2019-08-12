#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

from sklearn.decomposition import PCA

data = pd.read_csv('credit_card_train.csv', header=0)

# 对 'SEX', 'EDUCATION', 'MARRIAGE' 列独热编码
data = pd.get_dummies(data, columns=['SEX', 'EDUCATION', 'MARRIAGE'])

# 定义列名列表
columns = list(data.columns)

# 将 'DEFAULT' 移到最后
columns.remove('DEFAULT')
columns.append('DEFAULT')

# 重新排布列序
data = data.reindex(columns=columns)

# 定义特征和目标值
feature = data.iloc[:, 1:23].values
target = data['DEFAULT'].values
# 训练随机森林分类器
model = RandomForestClassifier()
model.fit(feature, target)

# 使用 .score() 方法获得准确率
score = model.score(feature, target)
print(score)

#0.9728571428571429

