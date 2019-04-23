#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

import sys
import csv

def get_city_dict():
    city_dict = {}

    with open('cities.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        for city in reader:
            city_dict[city[0]] = city[1]
    return city_dict

city_dict = get_city_dict()
#print(city_dict)

for city_name in city_dict.keys():
    print(city_name,end=' ') #如何不换行


#增加交互
input_city_name = input('\nplease input the city you want to search:')

city_url = city_dict.get(input_city_name)
if city_url:
    print(input_city_name,city_url)
else:
    print('Error!')
    sys.exit()
