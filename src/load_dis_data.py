# -*- coding: utf-8 -*-
"""
@Time ： 2022/4/12 9:40
@Auth ： zhcj
@File ：load_dis_data.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

from src.load_propagation_path_data import *
data = read_propagation_data()

def read_dis_data():

    vec_data = data["vec_data"]

    return vec_data


if __name__ == '__main__':
    new_vec = read_dis_data()

    print(new_vec)