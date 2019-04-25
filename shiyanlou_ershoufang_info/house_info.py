#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

import sys
import re
from bs4 import BeautifulSoup
import requests
import csv
# 成功打开页面时返回页面对象BeautifulSoup，否则打印错误信息，退出程序
def get_bsobj(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    # status_code==200时页面成功打开
    if html.status_code==200:
        html.encoding = 'utf-8'
        bsobj = BeautifulSoup(html.text, 'html.parser')
        return bsobj
    else:
        print('error!')
        sys.exit()

# 将页面中每一条房屋信息保存为一个字典，将所有的字典保存在列表中，返回列表
def get_house_info_list(url):
    house_info_list = []
    bsobj = get_bsobj(url)
    if not bsobj:
        return None
    house_list = bsobj.find_all('div',{'class':'info clear'})
    for house in house_list:
        title = house.find('div',{'class':'title'})
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

# 读取前三个页面的房屋信息，将信息保存到 house.csv 文件中
def house(url):
    house_info_list = []

    # 前3个页面
    for i in range(3):
        new_url = url+'pg'+str(i+1)
        house_info_list.extend(get_house_info_list(new_url))

    if house_info_list:
        with open('house.csv','w',encoding='utf-8') as f:
            # writer 对象，修改默认分隔符为 "|"
            writer = csv.writer(f, delimiter='|')
            for house_info in house_info_list:
                title = house_info.get("title").get_text()
                price = house_info.get("price")
                size = house_info.get("size")
                block = house_info.get("block")
                house_type = house_info.get("house_type")
                writer.writerow([title, int(price), int(size), block, house_type])                #print(block,price,size)
                print(house_info)

#print(house('https://sh.lianjia.com/ershoufang/xuhui/'))