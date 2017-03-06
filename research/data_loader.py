# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from __init__ import project_path


class DataLoader(object):

    data_map = {
        'shop_info.txt': ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt',
                          'shop_level', 'cate_1_name', 'cate_2_name', 'cate_3_name'],
        'user_pay.txt': ['user_id', 'shop_id', 'time_stamp'],
        'user_view.txt': ['user_id', 'shop_id', 'time_stamp'],
        'extra_user_view.txt': ['user_id', 'shop_id', 'time_stamp'],
    }

    @staticmethod
    def dump_data_frame(file_name=str(), columns=list()):
        raw_data = pd.read_csv(''.join([project_path, '/data/', file_name]))
        first_row_data = pd.DataFrame(dict(zip(columns, raw_data.columns)), index=[0])
        raw_data.columns = columns
        output_data = pd.concat([first_row_data, raw_data], axis=0)
        output_data.index = range(len(output_data.index))
        output_data = output_data[columns]
        return output_data

    @staticmethod
    def load_data(files=list()):
        if not files:
            files = DataLoader.data_map.keys()
        temp_data_set = dict()
        for current_file in files:
            current_data = DataLoader.dump_data_frame(current_file, DataLoader.data_map[current_file])
            temp_data_set[current_file.split('.')[0]] = current_data
        return temp_data_set

if __name__ == '__main__':
    data = DataLoader.load_data(files=['shop_info.txt'])
    print data['shop_info']
