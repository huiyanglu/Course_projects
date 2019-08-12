"""
Chapter 16.2
JSON格式
制作交易收盘价走势图
"""

from __future__ import (absolute_import,division,
                        print_function,unicode_literals)

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import json
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import pygal
import math
from itertools import groupby

"""
json_url = 'https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
response = urlopen(json_url)  # 2
# 读取数据
req = response.read()
# 将数据写入文件
with open('btc_close_2017_urllib.json', 'wb') as f:  # 3
    f.write(req)
# 加载json格式
file_urllib = json.loads(req.decode('utf8'))  # 4
print(file_urllib)
"""
"""
json_url = 'https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
# 读取数据
req = requests.get(json_url)
# 将数据写入文件
with open('btc_close_2017_urllib.json', 'w') as f:  # 3
    f.write(req.text)
file_requests = req.json()
print(file_requests)
"""

filename = 'btc_close_2017.json'
with open(filename) as f:
    btc_data = json.load(f)

dates,months,weeks,weekdays,close = [],[],[],[],[]
for btc_dict in btc_data:
    dates.append(btc_dict['date'])
    months.append(int(btc_dict['month']))
    weeks.append(int(btc_dict['week']))
    weekdays.append(btc_dict['weekday'])
    close.append(int(float(btc_dict['close'])))
    #print("{} is month {} week {}, {}, the close price is {} RMB".format(date,month,week,weekday,close))

def draw_line(x_data,y_data,title,y_legend):
    xy_map = []
    for x,y in groupby(sorted(zip(x_data,y_data)),key=lambda _:_[0]):
        y_list = [v for _,v in y]
        xy_map.append([x,sum(y_list)/len(y_list)])
    x_unique,y_mean = [*zip(*xy_map)]
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels=x_unique
    #N=20
    #line_chart.x_labels_major = dates[::N]
    #close_log = [math.log10(_) for _ in close] #用对数变换将非线性的趋势消除
    line_chart.add(y_legend,y_mean)
    line_chart.render_to_file(title+'.svg')
    return line_chart

idx_month = dates.index('2017-12-01')
line_chart_month = draw_line(months[:idx_month],close[:idx_month],'收盘价月日均值（￥）','月日均值')
line_chart_month

idx_week = dates.index('2017-12-11')
line_chart_week = draw_line(weeks[1:idx_week],close[1:idx_week],'收盘价周日均值（￥）','周日均价')
line_chart_week

with open('收盘价Dashboard.html','w',encoding='utf8') as html_file:
    html_file.write('<html><head><title>收盘价Dashboard</title><meta charset="utf-8"></head><body>\n')
    for svg in ['收盘价月日均值（￥）.svg','收盘价周日均值（￥）.svg']:
        html_file.write(
            '    <object type="image/svg+xml" data="{0}" height=500></object>\n'.format(svg))  # 1
    html_file.write('</body></html>')
