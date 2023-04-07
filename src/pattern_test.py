# -*- coding: utf-8 -*-
"""
@Time ： 2022/6/20 21:30
@Auth ： zhcj
@File ：pattern_test.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TKAgg')
import hypernetx as hnx
from sklearn import preprocessing
from sklearn.cluster import KMeans
import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import vq,kmeans,whiten
from functools import reduce
import Levenshtein
# from sklearn.decomposition import PCA
import warnings
from sklearn.manifold import TSNE
import re
import networkx as nx


# def generate_seq():
#     """
#         To generate the sequence
#     """
#     alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_period_vg_cluster.npy", allow_pickle=True).item()
#
#     algorithm_list = list(alg_cluster_data.keys())  # 将算法的名称转变为列表
#
#     alg_seq_data = {}
#     alg_i = "agr_1"
#     # for alg_i in algorithm_list:
#     filter_cluster = []
#     for period_j in alg_cluster_data[alg_i]:
#         # period = period_j["period"]
#         period_cluster = period_j["period_cluster"]
#
#         def filter_0(period_cluster):
#             """ 把0过滤掉，给period打上对应的分类标签 """
#             filter_period_list = []
#             for i in range(len(period_cluster)):
#                 # if period_cluster[i] != 0:
#                 if period_cluster[i]/sum(period_cluster) > 0.1:  # 单个数值的比例大于总数值的10%，则输出
#                     filter_period_list.append(i)
#
#             return filter_period_list
#
#         filter_cluster.append(filter_0(period_cluster))
#
#     print(filter_cluster)
#
#     fn = lambda x, code='|': reduce(lambda x, y: [str(i) + code + str(j) for i in x for j in y], x)
#     '''输入多个列表组成的列表, 输出其中每个列表所有元素可能的所有排列组合 code 用于分隔每个元素'''
#
#     result = fn(filter_cluster, ",")
#     seq_list = []
#     for str_i in result:
#         seq = str_i.strip().split(",")  # 以“ ， ”分割开，返回一个字符串列表
#         # intSeq = list(map(int, seq))  # 把对应的 seq 中所有的字符串类型转换成 整型列表
#         # seq_list.append(intSeq)
#         seq_list.append(seq)
#     F = apriori(seq_list, 0.5)
#     print(alg_i)
#     print('\nfrequent itemset:\n', F)
#     alg_seq_data[alg_i] = F
#
#     np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_seq" + '.npy', alg_seq_data)  # 保存
#
#     return alg_seq_data


def generate_seq():
    """
        To generate the sequence
    """
    alg_cluster_data = np.load(r"/static/temp_alg_period_vg_cluster.npy", allow_pickle=True).item()

    algorithm_list = list(alg_cluster_data.keys())  # 将算法的名称转变为列表

    alg_seq_data = {}
    # alg_i = "agr_1"
    for alg_i in algorithm_list:
        filter_cluster = []
        for period_j in alg_cluster_data[alg_i]:
            # period = period_j["period"]
            period_cluster = period_j["period_cluster"]

            def filter_0(period_cluster):
                """ 把0过滤掉，给period打上对应的分类标签 """
                filter_period_list = []
                for i in range(len(period_cluster)):
                    # if period_cluster[i] != 0:
                    if period_cluster[i]/sum(period_cluster) > 0:  # 单个数值的比例大于总数值的10%，则输出
                        filter_period_list.append(i)

                return filter_period_list

            filter_cluster.append(filter_0(period_cluster))

        print(filter_cluster)

        fn = lambda x, code='|': reduce(lambda x, y: [str(i) + code + str(j) for i in x for j in y], x)
        '''输入多个列表组成的列表, 输出其中每个列表所有元素可能的所有排列组合 code 用于分隔每个元素'''

        # control the length of sequence
        num = 5
        list_5 = []
        length = len(filter_cluster)
        count = 0
        pattern_seq_data = {}
        results = []  # 得到的去重过的序列总数

        while length >= num:
            for i in range(length):
                count += 1
                if count == num:
                    for itm in range(num):
                        list_5.append(filter_cluster[itm])
                    print(list_5)

                    result = fn(list_5, ",")
                    results.append(result)

                    filter_cluster.pop(0)  ## 删除第一个元素
                    length = len(filter_cluster)
                    count = 0
                    list_5 = []  ## 清空列表

        list_set = list(set(results))
        print(list_set)
        seq_list = []
        for str_i in list(set(results)):
            seq = str_i.strip().split(",")  # 以“ ， ”分割开，返回一个字符串列表
            # intSeq = list(map(int, seq))  # 把对应的 seq 中所有的字符串类型转换成 整型列表
            # seq_list.append(intSeq)
            seq_list.append(seq)
        F = apriori(seq_list, 0.5)
        print(alg_i)
        print('\nfrequent itemset:\n', F)


        alg_seq_data[alg_i] = F

    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_seq-" + str(num) + '.npy', alg_seq_data)  # 保存

    return alg_seq_data

#  序列频繁模式提取算法
def apriori(D, minSup):
    '''频繁项集用keys表示，
    key表示项集中的某一项，
    cutKeys表示经过剪枝步的某k项集。
    C表示某k项集的每一项在事务数据库D中的支持计数
    '''

    C1 = {}
    for T in D:
        for I in T:
            if I in C1:
                C1[I] += 1
            else:
                C1[I] = 1

    print(C1)
    _keys1 = C1.keys()

    keys1 = []
    for i in _keys1:
        keys1.append([i])

    n = len(D)
    cutKeys1 = []
    for k in keys1[:]:
        if C1[k[0]] * 1.0 / n >= minSup:
            cutKeys1.append(k)

    cutKeys1.sort()

    keys = cutKeys1
    all_keys = []
    while keys != []:
        C = getC(D, keys)
        print(C)
        cutKeys = getCutKeys(keys, C, minSup, len(D))
        for i in range(len(cutKeys)):
            all_keys.append((cutKeys[i], C[i]))
        # for key in cutKeys:
        #     all_keys.append(key)
        keys = aproiri_gen(cutKeys)

    return all_keys


def getC(D, keys):
    '''对keys中的每一个key进行计数'''
    C = []
    for key in keys:
        c = 0
        for T in D:
            have = True
            for k in key:
                if k not in T:
                    have = False
            if have:
                c += 1
        C.append(c)
    return C


def getCutKeys(keys, C, minSup, length):
    '''剪枝步'''
    for i, key in enumerate(keys):
        if float(C[i]) / length < minSup:
            keys.remove(key)
    return keys


def keyInT(key, T):
    '''判断项key是否在数据库中某一元组T中'''
    for k in key:
        if k not in T:
            return False
    return True


def aproiri_gen(keys1):
    '''连接步'''
    keys2 = []
    for k1 in keys1:
        for k2 in keys1:
            if k1 != k2:
                key = []
                for k in k1:
                    if k not in key:
                        key.append(k)
                for k in k2:
                    if k not in key:
                        key.append(k)
                key.sort()
                if key not in keys2:
                    keys2.append(key)

    return keys2


if __name__ == '__main__':
    data = generate_seq()
    print(data)