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

line_chart = pygal.Line(x_label_rotation=20,show_minor_x_labels=False)
line_chart.title = '收盘价￥'
line_chart.x_labels=dates
N=20
line_chart.x_labels_major = dates[::N]
line_chart.add('收盘价',close)
line_chart.render_to_file('收盘价折线图（￥）.svg')