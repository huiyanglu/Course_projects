#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
import requests
from_station = 'SHH'
to_station = 'CDW'
date = '2019-05-01'

url = ('https://kyfw.12306.cn/otn/leftTicket/queryO?'
       'leftTicketDTO.train_date={}&'
       'leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT').format(
            date, from_station, to_station
       )
url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
       'leftTicketDTO.train_date={}&'
       'leftTicketDTO.from_station={}&'
       'leftTicketDTO.to_station={}&purpose_codes=ADULT').format(date, from_station, to_station)
r = requests.get(url, verify=False)
print(r.json())
available_trains = r.json()['data']['result']
available_place = r.json()['data']['map']
options = ''.join([
    key for key, value in arguments.items() if value is True
])
TrainsCollection(available_trains,available_place, options).pretty_print()
