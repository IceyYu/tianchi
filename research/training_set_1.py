# -*- coding:utf-8 -*-
import re
import pandas as pd
import numpy as np
import pickle

weather_info = pickle.load(open('weather_info', 'r+'))
city_map = pickle.load(open('city_map', 'r+'))
user_pay_info = pickle.load(open('user_pay_info', 'r+'))
holiday_info = pickle.load(open('holiday_info','r+'))
weather_info_dict = pickle.load(open('weather_info_dict', 'r+'))
date_info = pickle.load(open('date_info', 'r+'))
base_collection = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score',
                   'comment_cnt', 'shop_level', 'cate_1_name', 'cate_2_name', 'cate_3_name']
dataset = []
for user in user_pay_info.keys():
    pay_data = user_pay_info[user]
    for date in pay_data.ordinary_dates:
        if date < '2015-07-01':
            continue
        training_data = [[], 0]
        training_data[0] += pay_data.get_attributes(base_collection)
        training_data[0] += [date]
        training_data[0] += weather_info_dict.get(city_map.get(pay_data.city_name, None), {}).get(date, [None]*5)
        training_data[0] += date_info[date]
        training_data[1] = pay_data.merchant_flow_dict[date]
        dataset.append(training_data)
feature = [doc[0] for doc in dataset]
label = [doc[1] for doc in dataset]

columns = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score',
           'comment_cnt', 'shop_level', 'cate_1_name', 'cate_2_name',
           'cate_3_name', 'date', 'high_temp', 'low_temp', 'rainy', 'wind_direction',
           'wind_force', 'month_counter', 'day_counter', 'holiday', 'businessday', 'weekday']
column_names = ['city_name', 'cate_1_name', 'cate_2_name', 'cate_3_name', 'wind_force']

d = pd.DataFrame(feature, columns=columns)

# 分天气
rainy_cate = {
    0: [re.compile('晴'), re.compile('多云'), re.compile('风')],
    1: [re.compile('阴'), re.compile('霾')],
    2: [re.compile('雨')],
    3: [re.compile('雪')]
}


def transfer_rainy_cate(x):
    if not x:
        return np.nan
    temp = [key for key, value in rainy_cate.iteritems() if
            reduce(lambda a, b: a + b, [re.findall(pattern, x) for pattern in value])]


d['rainy'] = d['rainy'].apply(transfer_rainy_cate)

# 分风力
wind_force_cate = {
    0: 3,
    1: 5,
    2: 6
}


def transfer_wind_force_cate(x):
    pattern = re.compile(r'\d')
    if not x or x < 0:
        return 0
    temp = re.findall(pattern, x)
    if not temp:
        return 0
    number = int(max(temp))
    if number <= 3:
        return 0
    elif number <= 5:
        return 1
    else:
        return 2


d['wind_force'] = d['wind_force'].apply(transfer_wind_force_cate)

maps = {}
for col in column_names:
    maps[col] = {value: key for key, value in enumerate(set(d[col]))}

reduced_column = [x for x in columns if x not in ['date', 'wind_direction']]

for column in column_names:
    d[column] = d[column].apply(lambda x: maps[column][x])

d = d[reduced_column]
d.fillna(value=-1, inplace=True)
d = d.applymap(int)


# 分温度
def transfer_temp_cate(x):
    if x < -20:
        return 0
    elif x < -10:
        return 1
    elif x < 0:
        return 2
    elif x < 10:
        return 3
    elif x < 20:
        return 4
    elif x < 30:
        return 5
    else:
        return 6


d[['high_temp', 'low_temp']] = d[['high_temp', 'low_temp']].applymap(transfer_temp_cate)