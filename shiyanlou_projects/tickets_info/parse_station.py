#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
import re
import requests
from pprint import pprint

#url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9100'
#网页源码中搜station_name找到链接
response = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
pprint(dict(stations), indent=4)

# python3 parse_station.py > stations.py 重定向到stations.py