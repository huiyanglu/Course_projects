#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
courses_ori = pd.read_csv('courses.txt',sep=',',header=0)

#创建时间索引 DatetimeIndex格式
i = pd.to_datetime(courses_ori['创建时间'])

courses_ts = pd.DataFrame(data=courses_ori.values,columns=courses_ori.columns,index=i)

courses_ts = courses_ts.drop('创建时间',axis=1) #去除原来的时间列

courses_ts_W = courses_ts.resample('W').sum()

courses_ts_W['id'] = range(0,len(courses_ts_W.index.values))

#Seaborn 提供的 regplot 方法，它可以在绘制散点图时，对数据自动进行回归拟合。
#sns.regplot("id", "学习时间", data=courses_ts_W, x_bins=10)

#plt.plot_date(courses_ts_W.index,courses_ts_W['学习时间'],'-')

courses_ts_A = courses_ts.copy()
courses_ts_A['平均学习时间'] = courses_ts_A['学习时间']/courses_ts_A['学习人数']
print(courses_ts_A.head())

courses_ts_A['平均学习时间/人数'] = courses_ts_A['平均学习时间']/courses_ts_A['学习人数']

# 学习平均学习时间与人数比值最为悬殊的前 10 条数据
#print(courses_ts_A.sort_values(by='平均学习时间/人数').head(10))

#plt.xlabel('Time series')
#plt.ylabel('Study time')
#plt.show()
from jieba import analyse

#提取关键词
a = []
for i in courses_ts_A['课程名称']:
    a.append(analyse.extract_tags(i,topK=2,withWeight=False, allowPOS=('eng','n','vn','v')))

keywords = pd.DataFrame(a,columns=['关键词1','关键词2'])
print(keywords.head())

courses_ts_C = courses_ts_A.copy()

#重置索引（最前面加了一列序号）
courses_ts_C = courses_ts_C.reset_index()

courses_ts_merged = pd.concat([courses_ts_C,keywords],axis=1).drop('创建时间',axis=1)
print(courses_ts_merged.head())

#将拥有不同值的变量转换为0/1数值
oneHot = pd.get_dummies(courses_ts_merged[['关键词1','关键词2']])
print(oneHot.head())

#引入PCA降维
from sklearn.decomposition import PCA
pca = PCA(n_components=5)
feature_pca = pca.fit_transform(oneHot)

from sklearn.cluster import k_means
from sklearn.metrics import silhouette_score

#建立模型
score = []
#依次轮廓系数
for i in range(10):
    model = k_means(feature_pca,n_clusters=i+2)
    score.append(silhouette_score(feature_pca,model[1]))
#轮廓系数绘图
plt.plot(range(2,12,1),score)
#plt.show()
#由图可知定K=6，即将课程聚为6类

#执行聚类
model = k_means(feature_pca,n_clusters=6)
#将类别列加入数据集中
courses_ts_final = pd.concat([courses_ts_merged,pd.Series(model[1],name='类别')],axis=1)
#根据类别排序并预览数据
print(courses_ts_final.sort_values(by='类别',ascending=False))


