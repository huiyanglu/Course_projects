#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.lianjia.com/city/'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

html = requests.get(url, headers=headers)
html.encoding ='utf-8'
bsobj = BeautifulSoup(html.text,'html.parser')

city_tags = bsobj.find('div',{'class':'city_list_section'}).find_all('a')

print(city_tags)

with open('cities.csv', 'w',encoding='utf-8') as f:
    for city_tag in city_tags:
        city_url = city_tag.get('href')
        city_name = city_tag.get_text()
        line1 = u'{0},'.format(city_name)
        line2 = u'{0}\n'.format(city_url)
        f.write(line1)
        f.write(line2)
