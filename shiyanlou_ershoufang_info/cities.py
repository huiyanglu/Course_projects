#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.lianjia.com/'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

# 获取html页面
html = requests.get(url, headers=headers)
html.encoding ='utf-8' #解码
# 获取BeautifulSoup对象（.text)
bsobj = BeautifulSoup(html.text,'html.parser')

# 得到div class='city_list_section'下所有 a 标签
#city_tags = bsobj.find('div',{'class':'city_list_section'}).find_all('a')
city_tags = bsobj.find('div',{'class':'link-list'}).div.dd.find_all('a')[1:]

print(city_tags)
"""
    city_tags 内数据的格式如下

    <a title="天津房产网" href="https://tj.lianjia.com/">天津</a>
    <a title="青岛房产网" href="https://qd.lianjia.com/">青岛</a>
    ...
"""

# 将每一条数据抽离，保存在csv文件中
with open('cities.csv', 'w',encoding='utf-8') as f:
    for city_tag in city_tags:
        city_url = city_tag.get('href')
        city_name = city_tag.get_text()
        line1 = u'{0},'.format(city_name)
        line2 = u'{0}\n'.format(city_url)
        f.write(line1)
        f.write(line2)
