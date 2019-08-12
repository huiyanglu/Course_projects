#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

import numpy as np

def find_outlier(data):
    outlier = []

    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    outlier_step = 1.5 * IQR
    for col in data:
        if (col < Q1 - outlier_step or col > Q3 + outlier_step):
            outlier.append(col)
    return outlier
