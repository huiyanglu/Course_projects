#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

import sys
import re
import csv
from bs4 import BeautifulSoup
import requests

def get_bsobj(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    if html.status_code==200:
        html.encoding = 'utf-8'
        bsobj = BeautifulSoup(html.text, 'html.parser')
        return bsobj
    else:
        print('error!')
        sys.exit()

def get_house_info_list(url):
    house_info_list = []
    bsobj = get_bsobj(url)
    if not bsobj:
        return None
    house_list = bsobj.find_all('div',{'class':'info clear'})
    for house in house_list:
        title = house.find('div',{'class':'title'}).get_text()
        info = house.find('div',{'class':'houseInfo'}).get_text().split('|')
        block = info[0].strip()
        house_type = info[1].strip()
        size_info = info[2].strip()
        size = re.findall(r'\d+',size_info)[0]
        price_info = house.find('div',{'class':'totalPrice'}).span.get_text()
        price = re.findall(r'\d+',price_info)[0]
        # 添加到列表中
        house_info_list.append({
            "title": title,
            "price": int(price),
            "size": int(size),
            "block": block,
            "house_type": house_type
        })
    return house_info_list

def house(url):
    house_info_list = []

    for i in range(3):
        new_url = url+'pg'+str(i+1)
        house_info_list.extend(get_house_info_list(new_url))

    if house_info_list:
        with open('house.csv','w',encoding='utf-8') as f:
            for house_info in house_info_list:
                title = house_info.get("title")
                price = house_info.get("price")
                size = house_info.get("size")
                block = house_info.get("block")
                house_type = house_info.get("house_type")
                line = u'{0} {1} {2} {3} {4}\n'.format(title,int(price),int(size),block,house_type)
                f.write(line)
                print(block,price,size)

#print(house('https://sh.lianjia.com/ershoufang/xuhui/'))