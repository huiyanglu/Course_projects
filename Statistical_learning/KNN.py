#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
# kd-tree每个结点中主要包含的数据结构如下
class KdNode(object):
    def __init__(self, dom_elt, split, left, right):
        self.dom_elt = dom_elt  # k维向量节点（k维空间中的一个样本点
        self.split = split  # 整数（进行分割维度的序号）
        self.left = left  # 该结点分割超平面左子空间构成的kd-tree
        self.right = right  # 该结点分割超平面右子空间构成的kd-tree


class KdTree(object):
    def __init__(self, data):
        k = len(data[0])  # 维度

        def CreateNode(split, data_set):
            if not data_set:  # 如果数据集为空
                return None

            data_set.sort(key=lambda x: x[split])  # 排序
            split_pos = len(data_set) // 2  # 找到中间位置的索引
            median = data_set[split_pos]  # 中位数分割点
            split_next = (split + 1) % k  # 下一个split分割点的索引

            return KdNode(median, split,
                          CreateNode(split_next, data_set[:split_pos]),
                          CreateNode(split_next, data_set[split_pos + 1:]))

        self.root = CreateNode(0, data)  # 从第0维分量开始构建kd树，返回根节点


# KDTree的前序遍历
def preorder(root):
    print(root.dom_elt)
    if root.left:
        preorder(root.left)
    if root.right:
        preorder(root.right)


# 对构建好的kd树进行搜索，寻找与目标点最近的样本点：
from math import sqrt
from collections import namedtuple

# 定义一个namedtuple,分别存放最近坐标点、最近距离和访问过的节点数
result = namedtuple("Result_tuple", "nearest_point  nearest_dist  nodes_visited")


def find_nearest(tree, point):
    k = len(point)  # 数据维度

    def travel(kd_node, target, r_dist):
        if kd_node is None:
            return result([0] * k, float("inf"), 0)  # python中用float("inf")和float("-inf")表示正负无穷

        nodes_visited = 1

        s = kd_node.split  # 进行分割的维度
        pivot = kd_node.dom_elt  # 进行分割的“轴”

        if target[s] <= pivot[s]:  # 如果目标点第s维小于分割轴的对应值(目标离左子树更近)
            nearer_node = kd_node.left  # 下一个访问节点为左子树根节点
            further_node = kd_node.right  # 同时记录下右子树
        else:  # 目标离右子树更近
            nearer_node = kd_node.right  # 下一个访问节点为右子树根节点
            further_node = kd_node.left

        temp1_area = travel(nearer_node, target, r_dist)  # 进行遍历找到包含目标点的区域

        nearest_rst = temp1_area.nearest_point  # 以此叶结点作为“当前最近点”
        dist_rst = temp1_area.nearest_dist  # 更新最近距离

        nodes_visited += temp1_area.nodes_visited

        if dist_rst < r_dist:
            r_dist = dist_rst  # 最近点将在以目标点为球心，max_dist为半径的超球体内

        dist_targetandsurface = abs(pivot[s] - target[s])  # 第s维上目标点与分割超平面的距离
        if r_dist < dist_targetandsurface:  # 判断超球体是否与超平面相交
            return result(nearest_rst, dist_rst, nodes_visited)  # 不相交则可以直接返回，不用继续判断

        # ----------------------------------------------------------------------
        # 计算目标点与分割点的欧氏距离
        p2_dist = sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(pivot, target)))

        if p2_dist < dist_rst:  # 如果“更近”
            nearest_rst = pivot  # 更新最近点
            dist_rst = p2_dist  # 更新最近距离
            r_dist = dist_rst  # 更新超球体半径

        # 检查另一个子结点对应的区域是否有更近的点
        temp2_another_area = travel(further_node, target, r_dist)

        nodes_visited += temp2_another_area.nodes_visited
        if temp2_another_area.nearest_dist < dist_rst:  # 如果另一个子结点内存在更近距离
            nearest_rst = temp2_another_area.nearest_point  # 更新最近点
            dist_rst = temp2_another_area.nearest_dist  # 更新最近距离

        return result(nearest_rst, dist_rst, nodes_visited)

    return travel(tree.root, point, float("inf"))  # 从根节点开始递归

data = [[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]]
kd = KdTree(data)
preorder(kd.root)

from time import clock
from random import random


# 产生一个k维随机向量，每维分量值在0~1之间
def random_point(k):
    return [random() for _ in range(k)]


# 产生n个k维随机向量
def random_points(k, n):
    return [random_point(k) for _ in range(n)]

ret = find_nearest(kd, [3,4.5])
print(ret)

N = 400000
t0 = clock()
kd2 = KdTree(random_points(3, N))            # 构建包含四十万个3维空间样本点的kd树
ret2 = find_nearest(kd2, [0.1,0.5,0.8])      # 四十万个样本点中寻找离目标最近的点
t1 = clock()
print ("time: ",t1-t0, "s")
print (ret2)