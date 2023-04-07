# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/7 9:53
@Auth ： zhcj
@File ：load_index_propagation_data.py
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
from scipy.cluster.vq import vq, kmeans, whiten
from functools import reduce
import Levenshtein
# from sklearn.decomposition import PCA
import warnings
from sklearn.manifold import TSNE
import re
import networkx as nx

# warnings.filterwarnings("ignore")



def process_hypergraph(hyper_data: str):
    """
    Returns hgraph, label dict
    """
    hgraph = {}
    label2id = {}
    vlabel2id = {}
    # label2id = {"a":"h1|h2", "b": "h3|h4", "c":"h5|h6"}
    # label2id = {'1':'v0', '2':'v1', '3':'v2', '4':'v3', '5':'v4'}
    he_id = 0
    v_id = 0
    for line in hyper_data.split("\n"):
        line = line.rstrip().rsplit(',')

        hyperedge, vertices = line[0], line[1:]
        if hyperedge != "":
            if hyperedge not in label2id.keys():
                hyperedge_label = re.sub('[\'\s]+', '', hyperedge)
                hyperedge_label = hyperedge_label.replace("\"", "")
                new_id = 'he'+str(he_id)
                # new_id = hyperedge
                he_id += 1
                label2id[hyperedge_label] = new_id
                hyperedge = new_id
            vertices_new = []
            for v in vertices:
                v_label = re.sub('[\'\s]+', '', v)
                v_label = v_label.replace("\"", "")
                if v_label != "":
                    if v_label not in vlabel2id.keys():
                        new_id = 'v'+str(v_id)
                        # new_id = v_label
                        v_id += 1
                        vlabel2id[v_label] = new_id
                        vertices_new.append(new_id)
                    else:
                        vertices_new.append(vlabel2id[v_label])
            vertices = vertices_new

            if hyperedge not in hgraph.keys():
                hgraph[hyperedge] = vertices
            else:
                hgraph[hyperedge] += vertices
    label_map = {ID: label for label, ID in label2id.items()}
    for label, ID in vlabel2id.items():
        label_map[ID] = label

    hgraph = hnx.Hypergraph(hgraph)
    hgraph = nx.readwrite.json_graph.node_link_data(hgraph.bipartite())
    # hgraph_dict = {hkey: list(vertices) for hkey, vertices in hgraph.incidence_dict.items()}

    return {"hyper_data": hgraph, "labels": label_map, "vlabel2id": vlabel2id }
    # return hgraph


    #  处理源节点对应的label
def process_seeds(seeds, vlabel2id):
    seeds_list = []
    i = 0
    while i < len(seeds):
        vg = seeds[i]
        seeds_list.append(vlabel2id[vg])
        i += 1

    return seeds_list

    #  找到包含源节点对应的超边list
def process_seeds_he(hgraph, seeds_list):
    seeds_he = []  # 原始传播对应的hg
    for i in hgraph["links"]:
        if i["target"] in seeds_list:
            seeds_he.append(i["source"])

    return list(set(seeds_he))  # 去重且顺序保持不变

    #  源节点对应超边的对应 待传播节点list
def process_he_list(hgraph, seeds_he):
    seeds_he_list = []
    for i in hgraph["links"]:
        if i["source"] in seeds_he:
            seeds_he_list.append(i["target"])

    return seeds_he_list

    #  传播路径对应的 v_list，加入源节点 seeds 中充当源节点
def load_propagation_path(seeds, vg_list):
    propagation_path = []  # 对应25步传播路径数组
    seeds_propagation = seeds + vg_list

    return seeds_propagation


    # 构造一个算法的数据格式 {'agr_1':{"seeds":[], "propagation_path":[]……}}
def read_algorithm_data(netName):
    path = "D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + netName + "_activited_nodes_bytime_dict.npy"
    algorithm_data = np.load(path, allow_pickle=True)
    alg_dict = {}  # 创建一个空的存储算法数据的字典
    # 遍历访问的字典所有的值
    for alg in algorithm_data.item():  # agl--str
        # 源节点的处理 ，访问到 seed_num_info
        alg_data = algorithm_data.item()[alg]
        seed_num_info = alg_data[0]["seed_num_info"]
        seeds = seed_num_info["seeds"]
        # 处理成需要的结果
        seed_list = []  # 源节点的格式
        for seed in seeds:
            seed = str(seed)
            seed_list.append(seed)

        # 传播路径的处理
        seed_num_info = alg_data[0]["seed_num_info"]
        mydict_length = seed_num_info["activated_seeds_bytime"].keys()
        mydict = {}  # 传播路径的格式
        # key_dictlist = []
        for key in mydict_length:
            key_dictlist = []
            activated_seed_bytime = seed_num_info["activated_seeds_bytime"][key]
            key = "P" + str(key)
            for value in activated_seed_bytime:
                key_dictlist.append(str(value))
            mydict[key] = key_dictlist

        alg_dict[alg] = {"seeds": seed_list, "propagation_path": mydict}

    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_data" + '.npy',
            alg_dict)  # 保存
    print(netName + "_temp_alg_data文件存储完毕！！！")

    return alg_dict


def read_per_node_index(netName):
    # 计算每个激活节点的指标
    hyper_data = open("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + "temp_data.csv")
    hyper_data = hyper_data.read()
    data = process_hypergraph(hyper_data)

    alg_data = read_algorithm_data(netName)  # 每个算法的系列数据
    hgraph = data["hyper_data"]
    vlabel2id = data["vlabel2id"]

    # 超边分类的数据
    Algebra_data = pd.read_csv("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + "temp_category_data.csv",
                               sep=',',
                               names=["he", "num"], index_col='he')
    # df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 7, 120], labels=[0, 1]))
    # df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 2, 4, 7, 10, 120], labels=[0, 1, 2, 3, 4])) # Algebra_data数据集的
    df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 3, 7, 14, 25, 90], labels=[0, 1, 2, 3, 4]))  # Music_Rev_data数据集的
    list1 = df_category.num.tolist()  # 类别个数

    category_list = []  # 定义一个新的存储分类类别的列表
    for i in range(len(set(list1))):
        category_list.append({'id': i, 'values': df_category[df_category.num == i].index.tolist()})
        # if i == 0:
        #     category_list.append(
        #         {'id': "small", 'values': df_category[df_category.num == i].index.tolist()})
        # elif i == 1:
        #     category_list.append(
        #         {'id': "large", 'values': df_category[df_category.num == i].index.tolist()})

    pie_dict = []
    per_alg_index_data = {}  # 对应阶段所包含节点的 struc features
    for alg in alg_data.keys():

        seeds = alg_data[alg]["seeds"]

        propagation_path = alg_data[alg]["propagation_path"]

        # # 把一个算法所有阶段包含的节点进行分类
        # all_nodes = seeds
        # for key in propagation_path.keys():
        #     vg_list = propagation_path[key]
        #
        #     all_nodes.extend(vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
        # print(all_nodes)


        #  写一个循环，得到 pie_data
        pie_data = []
        per_period_index_data = []
        for key in propagation_path.keys():
            vg_list = propagation_path[key]

            seeds_propagation = load_propagation_path(seeds, vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
            seeds = seeds_propagation

            per_vg_index_data = []
            for vg in seeds:
                vg_label = vlabel2id[vg]  # 处理源节点对应的label

                # # clustering coefficient
                # node_set = []
                # he_set = []
                # # 找到当前node的直接领接点
                # for itm in hgraph["links"]:
                #     if itm["source"] == vg_label:
                #         node_set.append(itm["target"])
                #     elif itm["target"] == vg_label:
                #         node_set.append(itm["source"])
                # # 找到邻接点集合中的点所构成边的数目
                # for itm in hgraph["links"]:
                #     if itm["source"] in node_set and itm["target"] in node_set:
                #         he_set.append(itm)

                # 所连 he
                per_vg_he_list = []
                for i in hgraph["links"]:
                    if i["target"] == vg_label:
                        per_vg_he_list.append(i["source"])

                # 所连 he 所连的待传播节点
                per_vg_degree_list = []
                for i in hgraph["links"]:
                    if (i["source"] in per_vg_he_list and i["target"] != vg_label):
                        per_vg_degree_list.append(i["target"])

                # 二阶领域的超边seeds_he 和 待传播节点seeds_he_list
                seeds_he = process_seeds_he(hgraph, per_vg_degree_list)  # 找到包含源节点对应的超边list
                seeds_he_list = process_he_list(hgraph, seeds_he)  # 源节点对应超边的对应 待传播节点list

                # list_0, list_1 = [], []
                # for obj in category_list:
                #     if obj["id"] == "small":
                #         for itm in per_vg_he_list:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
                #             if itm in obj["values"]:
                #                 list_0.append(itm)
                #     elif obj["id"] == "large":
                #         for itm in per_vg_he_list:
                #             if itm in obj["values"]:
                #                 list_1.append(itm)

                # 定义分五类的列表
                list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
                for obj in category_list:
                    if obj["id"] == 0:
                        for itm in per_vg_he_list:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
                            if itm in obj["values"]:
                                list_0.append(itm)
                    elif obj["id"] == 1:
                        for itm in per_vg_he_list:
                            if itm in obj["values"]:
                                list_1.append(itm)
                    elif obj["id"] == 2:
                        for itm in per_vg_he_list:
                            if itm in obj["values"]:
                                list_2.append(itm)
                    elif obj["id"] == 3:
                        for itm in per_vg_he_list:
                            if itm in obj["values"]:
                                list_3.append(itm)
                    else:
                        for itm in per_vg_he_list:
                            if itm in obj["values"]:
                                list_4.append(itm)

                # index
                node_degree = len(per_vg_degree_list)
                node_degree2 = len(set(per_vg_degree_list))  # 这是去重的节点度，不算是index中
                egonet_edges = len(per_vg_he_list)
                egonet_neighboring_degree = len(seeds_he_list)
                egonet_neighboring_edges = len(seeds_he)-egonet_edges
                average_degree = node_degree/egonet_edges  # average degree of neighborhood
                if egonet_neighboring_edges > 0:
                    average_alter_alter_num = egonet_neighboring_degree/egonet_neighboring_edges  # average number of neighbors of neighbors’ networks
                else:
                    average_alter_alter_num = 0
                clustering_coefficient = 2*egonet_edges/((node_degree2-1)*node_degree2)
                list_0_he_list = len(list_0)
                list_1_he_list = len(list_1)
                list_2_he_list = len(list_2)
                list_3_he_list = len(list_3)
                list_4_he_list = len(list_4)

                per_vg_index_data.append({
                    "vg_name": vg,
                    "vg_index": [node_degree, egonet_neighboring_degree, egonet_neighboring_edges, average_degree,
                               average_alter_alter_num, clustering_coefficient, list_0_he_list, list_1_he_list, list_2_he_list,
                                list_3_he_list, list_4_he_list]
                })
            per_period_index_data.append({
                "period": key,
                "period_index": per_vg_index_data
            })
        per_alg_index_data[alg] = per_period_index_data
    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_index" + '.npy', per_alg_index_data)  # 保存
    print(netName + "_temp_alg_index文件存储完毕！！！")

    return per_alg_index_data


def read_all_node_index(netName):
    # 计算网络中每个节点的指标
    hyper_data = open("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + "temp_data.csv")
    hyper_data = hyper_data.read()
    data = process_hypergraph(hyper_data)

    alg_data = read_algorithm_data(netName)  # 每个算法的系列数据
    hgraph = data["hyper_data"]
    vlabel2id = data["vlabel2id"]

    # 超边分类的数据
    Algebra_data = pd.read_csv("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + "temp_category_data.csv",
                               sep=',',
                               names=["he", "num"], index_col='he')
    df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 3, 7, 14, 25, 90], labels=[0, 1, 2, 3, 4]))  # Music_Rev_data数据集的
    list1 = df_category.num.tolist()  # 类别个数

    category_list = []  # 定义一个新的存储分类类别的列表
    for i in range(len(set(list1))):
        category_list.append({'id': i, 'values': df_category[df_category.num == i].index.tolist()})

    all_seeds = []  # 全部激活的节点
    for alg in alg_data.keys():
        seeds = alg_data[alg]["seeds"]
        propagation_path = alg_data[alg]["propagation_path"]

        for key in propagation_path.keys():
            vg_list = propagation_path[key]

            seeds_propagation = load_propagation_path(seeds, vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
            seeds = seeds_propagation
        all_seeds = load_propagation_path(all_seeds, seeds)

    all_seeds_quchong = list(set(all_seeds))

    all_node_index = []
    for vg in all_seeds_quchong:
        vg_label = vlabel2id[vg]  # 处理源节点对应的label

        # # clustering coefficient
        # node_set = []
        # he_set = []
        # # 找到当前node的直接领接点
        # for itm in hgraph["links"]:
        #     if itm["source"] == vg_label:
        #         node_set.append(itm["target"])
        #     elif itm["target"] == vg_label:
        #         node_set.append(itm["source"])
        # # 找到邻接点集合中的点所构成边的数目
        # for itm in hgraph["links"]:
        #     if itm["source"] in node_set and itm["target"] in node_set:
        #         he_set.append(itm)

        # 所连 he
        per_vg_he_list = []
        for i in hgraph["links"]:
            if i["target"] == vg_label:
                per_vg_he_list.append(i["source"])

        # 所连 he 所连的待传播节点
        per_vg_degree_list = []
        for i in hgraph["links"]:
            if (i["source"] in per_vg_he_list and i["target"] != vg_label):
                per_vg_degree_list.append(i["target"])

        # 二阶领域的超边seeds_he 和 待传播节点seeds_he_list
        seeds_he = process_seeds_he(hgraph, per_vg_degree_list)  # 找到包含源节点对应的超边list
        seeds_he_list = process_he_list(hgraph, seeds_he)  # 源节点对应超边的对应 待传播节点list

        # 定义分五类的列表
        list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
        for obj in category_list:
            if obj["id"] == 0:
                for itm in per_vg_he_list:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
                    if itm in obj["values"]:
                        list_0.append(itm)
            elif obj["id"] == 1:
                for itm in per_vg_he_list:
                    if itm in obj["values"]:
                        list_1.append(itm)
            elif obj["id"] == 2:
                for itm in per_vg_he_list:
                    if itm in obj["values"]:
                        list_2.append(itm)
            elif obj["id"] == 3:
                for itm in per_vg_he_list:
                    if itm in obj["values"]:
                        list_3.append(itm)
            else:
                for itm in per_vg_he_list:
                    if itm in obj["values"]:
                        list_4.append(itm)

        # index
        node_degree = len(per_vg_degree_list)
        node_degree2 = len(set(per_vg_degree_list))  # 这是去重的节点度，不算是index中
        egonet_edges = len(per_vg_he_list)
        egonet_neighboring_degree = len(seeds_he_list)
        egonet_neighboring_edges = len(seeds_he) - egonet_edges
        average_degree = node_degree / egonet_edges  # average degree of neighborhood
        if egonet_neighboring_edges > 0:
            average_alter_alter_num = egonet_neighboring_degree / egonet_neighboring_edges  # average number of neighbors of neighbors’ networks
        else:
            average_alter_alter_num = 0
        if ((node_degree2 - 1) * node_degree2) != 0:
            clustering_coefficient = 2 * egonet_edges / ((node_degree2 - 1) * node_degree2)
        else:
            clustering_coefficient = 0
        list_0_he_list = len(list_0)
        list_1_he_list = len(list_1)
        list_2_he_list = len(list_2)
        list_3_he_list = len(list_3)
        list_4_he_list = len(list_4)

        all_node_index.append({
            "vg_name": vg,
            "vg_index": [node_degree, egonet_neighboring_degree, egonet_neighboring_edges, average_degree,
                         average_alter_alter_num, clustering_coefficient, list_0_he_list, list_1_he_list,
                         list_2_he_list,
                         list_3_he_list, list_4_he_list]
        })
    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_all_alg_index" + '.npy', all_node_index)  # 保存
    print(netName + "_temp_all_alg_index文件存储完毕！！！")

    return all_node_index

# read_per_node_index
# def read_per_node_index(netName):
#     hyper_data = open("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + "temp_data.csv")
#     hyper_data = hyper_data.read()
#     data = process_hypergraph(hyper_data)
#
#     alg_data = read_algorithm_data(netName)  # 每个算法的系列数据
#     hgraph = data["hyper_data"]
#     vlabel2id = data["vlabel2id"]
#
#     # 超边分类的数据
#     Algebra_data = pd.read_csv("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + "temp_category_data.csv",
#                                sep=',',
#                                names=["he", "num"], index_col='he')
#     # df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 7, 120], labels=[0, 1]))
#     # df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 2, 4, 7, 10, 120], labels=[0, 1, 2, 3, 4])) # Algebra_data数据集的
#     df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 3, 7, 14, 25, 90], labels=[0, 1, 2, 3, 4]))  # Music_Rev_data数据集的
#     list1 = df_category.num.tolist()  # 类别个数
#
#     category_list = []  # 定义一个新的存储分类类别的列表
#     for i in range(len(set(list1))):
#         category_list.append({'id': i, 'values': df_category[df_category.num == i].index.tolist()})
#         # if i == 0:
#         #     category_list.append(
#         #         {'id': "small", 'values': df_category[df_category.num == i].index.tolist()})
#         # elif i == 1:
#         #     category_list.append(
#         #         {'id': "large", 'values': df_category[df_category.num == i].index.tolist()})
#
#     pie_dict = []
#     per_alg_index_data = {}  # 对应阶段所包含节点的 struc features
#     for alg in alg_data.keys():
#
#         seeds = alg_data[alg]["seeds"]
#
#         propagation_path = alg_data[alg]["propagation_path"]
#
#         # # 把一个算法所有阶段包含的节点进行分类
#         # all_nodes = seeds
#         # for key in propagation_path.keys():
#         #     vg_list = propagation_path[key]
#         #
#         #     all_nodes.extend(vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
#         # print(all_nodes)
#
#
#         #  写一个循环，得到 pie_data
#         pie_data = []
#         per_period_index_data = []
#         for key in propagation_path.keys():
#             vg_list = propagation_path[key]
#
#             seeds_propagation = load_propagation_path(seeds, vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
#             seeds = seeds_propagation
#
#             per_vg_index_data = []
#             for vg in seeds:
#                 vg_label = vlabel2id[vg]  # 处理源节点对应的label
#
#                 # # clustering coefficient
#                 # node_set = []
#                 # he_set = []
#                 # # 找到当前node的直接领接点
#                 # for itm in hgraph["links"]:
#                 #     if itm["source"] == vg_label:
#                 #         node_set.append(itm["target"])
#                 #     elif itm["target"] == vg_label:
#                 #         node_set.append(itm["source"])
#                 # # 找到邻接点集合中的点所构成边的数目
#                 # for itm in hgraph["links"]:
#                 #     if itm["source"] in node_set and itm["target"] in node_set:
#                 #         he_set.append(itm)
#
#                 # 所连 he
#                 per_vg_he_list = []
#                 for i in hgraph["links"]:
#                     if i["target"] == vg_label:
#                         per_vg_he_list.append(i["source"])
#
#                 # 所连 he 所连的待传播节点
#                 per_vg_degree_list = []
#                 for i in hgraph["links"]:
#                     if (i["source"] in per_vg_he_list and i["target"] != vg_label):
#                         per_vg_degree_list.append(i["target"])
#
#                 # 二阶领域的超边seeds_he 和 待传播节点seeds_he_list
#                 seeds_he = process_seeds_he(hgraph, per_vg_degree_list)  # 找到包含源节点对应的超边list
#                 seeds_he_list = process_he_list(hgraph, seeds_he)  # 源节点对应超边的对应 待传播节点list
#
#                 # list_0, list_1 = [], []
#                 # for obj in category_list:
#                 #     if obj["id"] == "small":
#                 #         for itm in per_vg_he_list:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
#                 #             if itm in obj["values"]:
#                 #                 list_0.append(itm)
#                 #     elif obj["id"] == "large":
#                 #         for itm in per_vg_he_list:
#                 #             if itm in obj["values"]:
#                 #                 list_1.append(itm)
#
#                 # 定义分五类的列表
#                 list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
#                 for obj in category_list:
#                     if obj["id"] == 0:
#                         for itm in per_vg_he_list:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
#                             if itm in obj["values"]:
#                                 list_0.append(itm)
#                     elif obj["id"] == 1:
#                         for itm in per_vg_he_list:
#                             if itm in obj["values"]:
#                                 list_1.append(itm)
#                     elif obj["id"] == 2:
#                         for itm in per_vg_he_list:
#                             if itm in obj["values"]:
#                                 list_2.append(itm)
#                     elif obj["id"] == 3:
#                         for itm in per_vg_he_list:
#                             if itm in obj["values"]:
#                                 list_3.append(itm)
#                     else:
#                         for itm in per_vg_he_list:
#                             if itm in obj["values"]:
#                                 list_4.append(itm)
#
#                 # index
#                 node_degree = len(per_vg_degree_list)
#                 node_degree2 = len(set(per_vg_degree_list))  # 这是去重的节点度，不算是index中
#                 egonet_edges = len(per_vg_he_list)
#                 egonet_neighboring_degree = len(seeds_he_list)
#                 egonet_neighboring_edges = len(seeds_he)-egonet_edges
#                 average_degree = node_degree/egonet_edges  # average degree of neighborhood
#                 if egonet_neighboring_edges > 0:
#                     average_alter_alter_num = egonet_neighboring_degree/egonet_neighboring_edges  # average number of neighbors of neighbors’ networks
#                 else:
#                     average_alter_alter_num = 0
#                 clustering_coefficient = 2*egonet_edges/((node_degree2-1)*node_degree2)
#                 list_0_he_list = len(list_0)
#                 list_1_he_list = len(list_1)
#                 list_2_he_list = len(list_2)
#                 list_3_he_list = len(list_3)
#                 list_4_he_list = len(list_4)
#
#                 per_vg_index_data.append({
#                     "vg_name": vg,
#                     "vg_index": [node_degree, egonet_neighboring_degree, egonet_neighboring_edges, average_degree,
#                                average_alter_alter_num, clustering_coefficient, list_0_he_list, list_1_he_list, list_2_he_list,
#                                 list_3_he_list, list_4_he_list]
#                 })
#             per_period_index_data.append({
#                 "period": key,
#                 "period_index": per_vg_index_data
#             })
#         per_alg_index_data[alg] = per_period_index_data
#     np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_index" + '.npy', per_alg_index_data)  # 保存
#     print(netName + "_temp_alg_index文件存储完毕！！！")
#
#     return per_alg_index_data

def cluster_all_vg_node(netName):
    """"
        得到每个算法的全部节点的分类结果
    """
    # alg_index_data = read_per_node_index(netName)
    alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy",
                               allow_pickle=True).item()


    # 聚类---降维---一个网络的所有节点
    all_node_index = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_all_alg_index.npy",
                               allow_pickle=True)

    vg_name_list = []
    vg_index_list = []
    for vg in all_node_index:
        vg_name_list.append(vg["vg_name"])
        vg_index_list.append(vg["vg_index"])

    vg_index0 = np.array(vg_index_list)
    vg_index1 = pd.DataFrame(vg_index0)
    vg_index1.insert(0, "vg", vg_name_list, allow_duplicates=False)

    # # 数据规整化处理及k-means聚类
    svg_index = vg_index1.drop(['vg'], axis=1)

    points = svg_index.values
    # 将原始数据做归一化处理
    data = whiten(points)

    centroid = kmeans(data, 5)[0]  # 分为5类
    # print(centroid)  # 输出中心
    # 使用vq函数根据聚类中心对所有数据进行分类,vq的输出也是两维的,[0]表示的是所有数据的label
    label = vq(data, centroid)[0]
    # print(label)

    # 归一化数据  降维 看降维效果
    tsne = TSNE()
    data1 = tsne.fit_transform(data)  # 进行数据降维,并返回结果
    data1 = pd.DataFrame(data1, index=label)
    data_tsne = pd.DataFrame(tsne.embedding_, index=data1.index)
    ## 新添
    data_tsne.columns = ["x", "y"]
    X = data_tsne["x"].tolist()
    Y = data_tsne["y"].tolist()
    scatters1 = [list(item) for item in zip(label, vg_name_list)]  # 转换成一个以列表构成的列表
    scatters2 = [list(item) for item in zip(X, Y)]

    scatters = []
    scatter = []
    for i in range(len(scatters1)):
        scatter.append(scatters1[i][0])
        scatter.append(scatters1[i][1])
        scatter.append(scatters2[i][0])
        scatter.append(scatters2[i][1])
        scatters.append(scatter)
        scatter = []
    warnings.filterwarnings("ignore")

    all_cluster_list = []
    all_results = [list(item) for item in zip(label, vg_name_list)]  # 转换成一个以列表构成的列表

    # 定义分五类的列表
    all_list_0, all_list_1, all_list_2, all_list_3, all_list_4 = [], [], [], [], []
    for all_result in all_results:
        if all_result[0] == 0:
            all_list_0.append(all_result[1])
        elif all_result[0] == 1:
            all_list_1.append(all_result[1])
        elif all_result[0] == 2:
            all_list_2.append(all_result[1])
        elif all_result[0] == 3:
            all_list_3.append(all_result[1])
        else:
            all_list_4.append(all_result[1])

    all_cluster_num = [len(all_list_0), len(all_list_1), len(all_list_2), len(all_list_3), len(all_list_4)]

    all_cluster_list.append({
        "all_cluster": all_cluster_num,
        "cluster_list": [{'id': str(0), 'values': all_list_0}, {'id': str(1), 'values': all_list_1},
                         {'id': str(2), 'values': all_list_2}, {'id': str(3), 'values': all_list_3},
                         {'id': str(4), 'values': all_list_4}]
    })

    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_all_alg_cluster" + '.npy',
            all_cluster_list)  # 保存
    print(netName + "_temp_all_alg_cluster文件存储完毕！！！")


    # 每个算法的聚类和降维的结果
    per_alg_cluster = {}
    per_alg_scatter = {}
    for alg_i in alg_index_data:
        period_cluster_list = []
        alg_scatters = []
        for period_j in alg_index_data[alg_i]:
            if period_j["period"] == "P24":
                period = period_j["period"]
                period_index = period_j["period_index"]
                alg_vg_name_list = []
                for alg_vg in period_index:
                    alg_vg_name_list.append(alg_vg["vg_name"])

                # 从scatters中提取该算法的聚类和降维结构
                alg_label, alg_X, alg_Y = [], [], []
                for vg_i in alg_vg_name_list:
                    for item in scatters:
                        if vg_i == item[1]:
                            alg_label.append(item[0])
                            alg_X.append(item[2])
                            alg_Y.append(item[3])

                alg_scatters1 = [list(item) for item in zip(alg_label, alg_vg_name_list)]  # 转换成一个以列表构成的列表
                alg_scatters2 = [list(item) for item in zip(alg_X, alg_Y)]

                alg_scatter = []
                for i in range(len(alg_scatters1)):
                    alg_scatter.append(alg_scatters1[i][0])
                    alg_scatter.append(alg_scatters1[i][1])
                    alg_scatter.append(alg_scatters2[i][0])
                    alg_scatter.append(alg_scatters2[i][1])
                    alg_scatters.append(alg_scatter)
                    alg_scatter = []

                results = [list(item) for item in zip(alg_label, alg_vg_name_list)]  # 转换成一个以列表构成的列表

                # 定义分五类的列表
                list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
                for result in results:
                    if result[0] == 0:
                        list_0.append(result[1])
                    elif result[0] == 1:
                        list_1.append(result[1])
                    elif result[0] == 2:
                        list_2.append(result[1])
                    elif result[0] == 3:
                        list_3.append(result[1])
                    else:
                        list_4.append(result[1])

                vg_cluster_num = [len(list_0), len(list_1), len(list_2), len(list_3), len(list_4)]

                period_cluster_list.append({
                    "period": period,
                    "period_cluster": vg_cluster_num,
                    "cluster_list": [{'id': str(0), 'values': list_0}, {'id': str(1), 'values': list_1},
                                     {'id': str(2), 'values': list_2}, {'id': str(3), 'values': list_3},
                                     {'id': str(4), 'values': list_4}]
                })

        per_alg_cluster[alg_i] = period_cluster_list
        per_alg_scatter[alg_i] = scatters

    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_cluster" + '.npy',
            per_alg_cluster)  # 保存
    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_scatter" + '.npy',
            per_alg_scatter)  # 保存
    print(netName + "_temp_alg_cluster文件存储完毕！！！")
    print(netName + "_temp_alg_scatter文件存储完毕！！！")

    return per_alg_cluster

# cluster_all_vg_node-----origin
# def cluster_all_vg_node(netName):
#     """"
#         得到每个算法的全部节点的分类结果
#     """
#     # alg_index_data = read_per_node_index(netName)
#     alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy",
#                                allow_pickle=True).item()
#     per_alg_cluster = {}
#     per_alg_scatter = {}
#     for alg_i in alg_index_data:
#         period_cluster_list = []
#         scatters = []
#         for period_j in alg_index_data[alg_i]:
#             if period_j["period"] == "P24":
#                 period = period_j["period"]
#                 period_index = period_j["period_index"]
#                 vg_name_list = []
#                 vg_index_list = []
#                 for vg in period_index:
#                     vg_name_list.append(vg["vg_name"])
#                     vg_index_list.append(vg["vg_index"])
#
#                 vg_index0 = np.array(vg_index_list)
#                 # # 数据降维(4)
#                 # pca = PCA(n_components=4, copy=True, whiten=False)  # 降到四维
#                 # pca.fit(vg_index0)  # train
#                 # newX = pca.fit_transform(vg_index0)
#                 # vg_index1 = pd.DataFrame(newX)
#                 vg_index1 = pd.DataFrame(vg_index0)
#                 vg_index1.insert(0, "vg", vg_name_list, allow_duplicates=False)
#                 # vg_index1.to_csv(r"C:\Users\01\Desktop\rd_index.csv")
#
#                 # # 数据规整化处理及k-means聚类
#                 svg_index = vg_index1.drop(['vg'], axis=1)
#                 # # svg_index_scaled = preprocessing.scale(svg_index) # 数据规整化处理
#                 # #
#                 # # myKmeans = KMeans(algorithm='auto', n_clusters=5, n_init=10, max_iter=200)
#                 # # myKmeans.fit(svg_index_scaled)
#                 # # vg_cluster_result = myKmeans.predict(svg_index).tolist()
#
#                 points = svg_index.values
#                 # 将原始数据做归一化处理
#                 data = whiten(points)
#
#                 centroid = kmeans(data, 5)[0]  # 分为5类
#                 print(centroid)  # 输出中心
#                 # 使用vq函数根据聚类中心对所有数据进行分类,vq的输出也是两维的,[0]表示的是所有数据的label
#                 label = vq(data, centroid)[0]
#                 print(label)
#
#                 # 归一化数据  降维 看降维效果
#                 tsne = TSNE()
#                 data1 = tsne.fit_transform(data)  # 进行数据降维,并返回结果
#                 data1 = pd.DataFrame(data1, index=label)
#                 data_tsne = pd.DataFrame(tsne.embedding_, index=data1.index)
#                 ## 新添
#                 data_tsne.columns = ["x", "y"]
#                 X = data_tsne["x"].tolist()
#                 Y = data_tsne["y"].tolist()
#                 scatters1 = [list(item) for item in zip(label, vg_name_list)]  # 转换成一个以列表构成的列表
#                 scatters2 = [list(item) for item in zip(X, Y)]
#
#                 scatter = []
#                 for i in range(len(scatters1)):
#                     scatter.append(scatters1[i][0])
#                     scatter.append(scatters1[i][1])
#                     scatter.append(scatters2[i][0])
#                     scatter.append(scatters2[i][1])
#                     scatters.append(scatter)
#                     scatter = []
#
#                 print(data_tsne)
#                 #
#                 # # 根据类别分割数据后，画图
#                 # d = data_tsne[data_tsne.index == 0]  # 找出聚类类别为0的数据对应的降维结果
#                 # plt.scatter(d[0], d[1], c='lightgreen', marker='o')
#                 # d = data_tsne[data_tsne.index == 1]
#                 # plt.scatter(d[0], d[1], c='orange', marker='o')
#                 # d = data_tsne[data_tsne.index == 2]
#                 # plt.scatter(d[0], d[1], c='lightblue', marker='o')
#                 # d = data_tsne[data_tsne.index == 3]
#                 # plt.scatter(d[0], d[1], c='green', marker='o')
#                 # d = data_tsne[data_tsne.index == 4]
#                 # plt.scatter(d[0], d[1], c='blue', marker='o')
#                 # d = data_tsne[data_tsne.index == 5]
#                 # plt.scatter(d[0], d[1], c='red', marker='o')
#                 # d = data_tsne[data_tsne.index == 6]
#                 # plt.scatter(d[0], d[1], c='black', marker='o')
#                 # plt.show()
#
#                 warnings.filterwarnings("ignore")
#                 # warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=793)
#
#                 results = [list(item) for item in zip(label, vg_name_list)]  # 转换成一个以列表构成的列表
#
#                 # 定义分五类的列表
#                 list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
#                 for result in results:
#                     if result[0] == 0:
#                         list_0.append(result[1])
#                     elif result[0] == 1:
#                         list_1.append(result[1])
#                     elif result[0] == 2:
#                         list_2.append(result[1])
#                     elif result[0] == 3:
#                         list_3.append(result[1])
#                     else:
#                         list_4.append(result[1])
#
#                 vg_cluster_num = [len(list_0), len(list_1), len(list_2), len(list_3), len(list_4)]
#
#                 # _num = [{'id': str(0), 'values': len(list_0)}, {'id': str(1), 'values': len(list_1)},
#                 #         {'id': str(2), 'values': len(list_2)}, {'id': str(3), 'values': len(list_3)},
#                 #         {'id': str(4), 'values': len(list_4)}]
#
#                 # #  结果输出
#                 # def print_kmcluster(k):
#                 #     '''用于聚类结果的输出k：为聚类中心个数'''
#                 #     for i in range(k):
#                 #         print('聚类', i)
#                 #         ls = []
#                 #         for index, value in enumerate(vg_cluster_result):
#                 #             if i == value:
#                 #                 ls.append(index)
#                 #         print(vg_index1.loc[ls, ['vg', '0', '5', '8']])
#                 #
#                 # print_kmcluster(5)
#
#                 period_cluster_list.append({
#                     "period": period,
#                     "period_cluster": vg_cluster_num,
#                     "cluster_list": [{'id': str(0), 'values': list_0}, {'id': str(1), 'values': list_1},
#                                      {'id': str(2), 'values': list_2}, {'id': str(3), 'values': list_3},
#                                      {'id': str(4), 'values': list_4}]
#                 })
#
#         per_alg_cluster[alg_i] = period_cluster_list
#         per_alg_scatter[alg_i] = scatters
#
#     np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_cluster" + '.npy',
#             per_alg_cluster)  # 保存
#     np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_scatter" + '.npy',
#             per_alg_scatter)  # 保存
#     print(netName + "_temp_alg_cluster文件存储完毕！！！")
#     print(netName + "_temp_alg_scatter文件存储完毕！！！")
#
#     return per_alg_cluster

def cluster_vg_node(netName):
    """
        得到每个算法每个阶段的聚类结果
    """
    alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_cluster.npy", allow_pickle=True).item()
    alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy", allow_pickle=True).item()

    per_period_cluster = {}
    for alg_i in alg_index_data:
        period_cluster_list = []
        alg_cluster_list = alg_cluster_data[alg_i][0]["cluster_list"]
        for period_j in alg_index_data[alg_i]:
            period = period_j["period"]
            period_index = period_j["period_index"]
            vg_name_list = []
            for vg in period_index:
                vg_name_list.append(vg["vg_name"])

            # 定义分五类的列表
            list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
            for obj in alg_cluster_list:
                if obj["id"] == "0":
                    for itm in vg_name_list:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
                        if itm in obj["values"]:
                            list_0.append(itm)
                elif obj["id"] == "1":
                    for itm in vg_name_list:
                        if itm in obj["values"]:
                            list_1.append(itm)
                elif obj["id"] == "2":
                    for itm in vg_name_list:
                        if itm in obj["values"]:
                            list_2.append(itm)
                elif obj["id"] == "3":
                    for itm in vg_name_list:
                        if itm in obj["values"]:
                            list_3.append(itm)
                else:
                    for itm in vg_name_list:
                        if itm in obj["values"]:
                            list_4.append(itm)

            vg_cluster_num = [len(list_0), len(list_1), len(list_2), len(list_3), len(list_4)]

            period_cluster_list.append({
                "period": period,
                "period_cluster": vg_cluster_num,
                "cluster_list": [{'id': str(0), 'values': list_0}, {'id': str(1), 'values': list_1},
                                 {'id': str(2), 'values': list_2}, {'id': str(3), 'values': list_3},
                                 {'id': str(4), 'values': list_4}]
            })

        per_period_cluster[alg_i] = period_cluster_list

    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_period_vg_cluster" + '.npy',
            per_period_cluster)  # 保存
    print(netName + "_temp_alg_period_vg_cluster文件存储完毕！！！")

    return per_period_cluster

#  得到不同算法, 传播路径的的系列数据 pie_dict 存储在data中调用
def read_propagation_data():
    # hyper_data = open('D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_data.csv')
    # hyper_data = open(r'/static/temp_files/temp_data.csv')
    hyper_data = open(r'D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_data.csv')
    hyper_data = hyper_data.read()
    data = process_hypergraph(hyper_data)

    alg_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_data.npy",
                       allow_pickle=True).item()  # 算法的系列数据

    # ============传播=========== ## data = hgraph
    hgraph = data["hyper_data"]
    vlabel2id = data["vlabel2id"]

    # # seeds = ["1"]   # 原始传播节点
    # seeds = ['101', '12', '15', '76', '32', '52', '27', '44', '121', '37', '7', '18', '29', '51', '14', '155', '136',
    #          '55', '42', '156', '0', '130', '158', '11', '95']
    #
    # # seeds = ['155']
    #
    # # 传播路径的25步
    # propagation_path = {'P0': ['140', '66', '38'], 'P1': [], 'P2': ['4', '58', '203'], 'P3': ['303', '193', '22'],
    #                     'P4': ['216', '91'], 'P5': ['10', '94', '237', '173', '135'],
    #                     'P6': ['8', '28', '169', '163', '345', '349', '17', '154', '125'], 'P7': ['30'],
    #                     'P8': ['197', '2', '257'], 'P9': ['97', '170', '56', '74'],
    #                     'P10': ['63', '93', '318', '49', '21'], 'P11': ['183', '174', '290', '181', '322', '57'],
    #                     'P12': ['214', '230', '242', '126'], 'P13': ['248', '20', '33'],
    #                     'P14': ['201', '330', '199', '321', '31', '102'],
    #                     'P15': ['151', '147', '279', '105', '234', '143'],
    #                     'P16': ['179', '238', '157', '36', '222', '223', '184', '210'],
    #                     'P17': ['116', '243', '64', '239', '5', '167', '211'], 'P18': ['82', '176', '39', '35', '110'],
    #                     'P19': ['134', '164', '19', '60', '104', '240', '83', '23', '59', '229', '119'],
    #                     'P20': ['69', '208', '54', '191', '304', '40', '142'],
    #                     'P21': ['254', '50', '109', '71', '297', '148', '250', '123', '192'],
    #                     'P22': ['185', '120', '67', '265', '177'], 'P23': ['175', '80', '196', '85'],
    #                     'P24': ['329', '334', '215', '217']}

    pie_dict = []
    vec_data = []
    for alg in alg_data.keys():

        seeds = alg_data[alg]["seeds"]

        propagation_path = alg_data[alg]["propagation_path"]

        #  写一个循环，得到 pie_data
        pie_data = []
        agr_vec_data = []
        for key in propagation_path.keys():

            vg_list = propagation_path[key]

            # seeds_propagation = load_propagation_path(seeds, vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
            # seeds = seeds_propagation

            seeds = vg_list

            seeds_data = {}
            # seeds = ["1"]   # 原始传播节点
            seeds_list = process_seeds(seeds, vlabel2id)  # 处理源节点对应的label
            seeds_data["seeds_list"] = seeds_list
            seeds_he = process_seeds_he(hgraph, seeds_list)  # 找到包含源节点对应的超边list

            seeds_data["seeds_he"] = seeds_he
            # seeds_he_list = process_he_list(hgraph, seeds_he)  #  源节点对应超边的对应 待传播节点list
            # seeds_data["seeds_he_list"] = seeds_he_list
            # print(seeds_data)

            data["seeds_data"] = seeds_data
            # print(data)

            # =============== 处理节点领域结构的 part =================
            # Algebra_data = pd.read_csv( "D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_category_data.csv" , sep=',', names=["he", "num"], index_col='he')
            # print(Algebra_data)
            Algebra_data = pd.read_csv(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_category_data.csv", sep=',', names=["he", "num"], index_col='he')
            # df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 2, 4, 7, 10, 120], labels=[0, 1, 2, 3, 4])) # Algebra_data数据集的
            df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 3, 7, 14, 25, 90], labels=[0, 1, 2, 3, 4]))  # Music_Rev_data数据集的
            # print(df_category)
            list1 = df_category.num.tolist()  # 类别个数

            category_list = []  # 定义一个新的存储分类类别的列表
            for i in range(len(set(list1))):
                category_list.append({'id': i, 'values': df_category[df_category.num == i].index.tolist()})
            # print(category_list)
            # 定义分五类的列表
            list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
            for obj in category_list:
                if obj["id"] == 0:
                    for itm in seeds_he:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
                        if itm in obj["values"]:
                            list_0.append(itm)
                elif obj["id"] == 1:
                    for itm in seeds_he:
                        if itm in obj["values"]:
                            list_1.append(itm)
                elif obj["id"] == 2:
                    for itm in seeds_he:
                        if itm in obj["values"]:
                            list_2.append(itm)
                elif obj["id"] == 3:
                    for itm in seeds_he:
                        if itm in obj["values"]:
                            list_3.append(itm)
                else:
                    for itm in seeds_he:
                        if itm in obj["values"]:
                            list_4.append(itm)

            #  此阶段的分类别的超边列表构成的字典，形式类似 category_list
            list_dict = [{'id': 0, 'values': list_0}, {'id': 1, 'values': list_1}, {'id': 2, 'values': list_2},
                         {'id': 3, 'values': list_3}, {'id': 4, 'values': list_4}]
            # print(list_dict)
            # print(list_0)
            # print(list_1)
            # print(list_2)
            # print(list_3)
            # print(list_4)

            # 分类别获取此阶段的传播节点所连接超边的待传播节点数量
            num_list = []
            for d in list_dict:
                num_list.append(len(d["values"]))

            agr_vec_data.append(num_list)
            # print(num_list)

                # num_1 = []
                # for i in d['values']:
                #     num = Algebra_data.loc[i, "num"]
                #     num_1.append(num)
                # num_list.append(sum(num_1))
            # print(num_list)

            # with open(r'C:\Users\01\Desktop\test.csv', "a+", newline="") as csv_file:
            #     csv_writer = csv.writer(csv_file, delimiter=',')
            #     csv_writer.writerow(['Period', 0, 1, 2, 3, 4])
            #     csv_writer.writerow(["P0", num_list[0], num_list[1], num_list[2], num_list[3], num_list[4]])
            #     print("成功保存CSV文件……")

            pie_data.append({
                "period": key,
                "sum": str(sum(num_list)),
                "category_num": list(set(list1)),
                "category_list":
                    [{'id': str(0), 'values': str(num_list[0])}, {'id': str(1), 'values': str(num_list[1])},
                     {'id': str(2), 'values': str(num_list[2])},
                     {'id': str(3), 'values': str(num_list[3])}, {'id': str(4), 'values': str(num_list[4])}],
                "vg_list": vg_list,
                "category": category_list,
                "algorithm": alg
            })
        pie_dict.append({"name": alg, "values": pie_data})

        vec_data.append({"name": alg, "vector": agr_vec_data})

    # data["pie_data"] = pie_data
    data["pie_dict"] = pie_dict
    data["vec_data"] = vec_data

    return data


if __name__ == '__main__':
    # data = cluster_vg_node("Music-Rev")
    data = cluster_all_vg_node("Music-Rev")
    # data = read_per_node_index("Music-Rev")
    # data = read_all_node_index("Music-Rev")
    # data = read_propagation_data()
    # data = read_algorithm_data("Music-Rev")

    print(data)

