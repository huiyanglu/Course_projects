#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

import sys
import csv
import requests
from bs4 import BeautifulSoup
from house_info import house

def get_city_dict():
    city_dict = {}

    with open('cities.csv','r',encoding='utf-8') as f:
        reader = csv.reader(f)
        for city in reader:
            city_dict[city[0]] = city[1]
    return city_dict

def get_district_dict(url):
    district_dict = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'
    bsobj = BeautifulSoup(html.text, 'html.parser')

    district_tags = bsobj.find('div',{'data-role':'ershoufang'}).find_all('a')
    #print(district_tags)
    for tag in district_tags:
        district_url = tag.get('href')
        district_name = tag.get_text()
        district_dict[district_name] = district_url
    print(district_dict)
    return district_dict


def run():
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

    #ershoufang_city_url = city_url + 'ershoufang'
    ershoufang_city_url = city_url

    district_dict = get_district_dict(ershoufang_city_url)
    for district_name in district_dict.keys():
        print(district_name,end=' ') #如何不换行

    # 增加交互
    input_district_name = input('\nplease input the district:')

    district_url = district_dict.get(input_district_name)
    if district_url:
        print(input_district_name, district_url)
    else:
        print('Error!')
        sys.exit()

    #house_info_url = city_url+district_url[1:]
    house_info_url = city_url + district_url[12:]

    print(house_info_url)
    house(house_info_url)

if __name__ == '__main__':
    run()

