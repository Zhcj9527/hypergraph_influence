from flask import render_template, request, url_for, jsonify, redirect, Response, send_from_directory
from app import app
import json
import numpy as np
import pandas as pd
import hypernetx as hnx
import re
import networkx as nx
import csv
# from tqdm import tqdm
from os import path
import os
import copy
import collections

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
    label_map = {ID:label for label, ID in label2id.items()}
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
    for i in seeds:
        if i in vlabel2id.keys():
            seeds_list.append(vlabel2id[i])
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


if __name__ == '__main__':
    # hyper_data = open('static/hyper_top5.csv')
    hyper_data = open('../static/Algebra_data.csv')
    hyper_data = hyper_data.read()
    data = process_hypergraph(hyper_data)


    # ============传播=========== ## data = hgraph
    hgraph = data["hyper_data"]
    vlabel2id = data["vlabel2id"]

    # seeds = ["1"]   # 原始传播节点
    seeds = ['101', '12', '15', '76', '32', '52', '27', '44', '121', '37', '7', '18', '29', '51', '14', '155', '136',
             '55', '42', '156', '0', '130', '158', '11', '95', '140', '66', '38', '4', '58', '203']

    # seeds = ['155']

    # vg_list = ['1', '35']

    # vg_list = ['140', '66', '38']  # 传播路径对应的节点 第一阶段
    # vg_list = []                    # 传播路径对应的节点 第二阶段
    # vg_list = ['4', '58', '203']  # 传播路径对应的节点 第三阶段
    vg_list = ['303', '193', '22']  # 传播路径对应的节点 第四阶段

    seeds_propagation = load_propagation_path(seeds, vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
    # # print(seeds_propagation)
    #
    seeds = seeds_propagation

    seeds_data = {}
    # seeds = ["1"]   # 原始传播节点
    seeds_list = process_seeds(seeds, vlabel2id)  #  处理源节点对应的label
    seeds_data["seeds_list"] = seeds_list
    seeds_he = process_seeds_he(hgraph, seeds_list)  #  找到包含源节点对应的超边list
    seeds_data["seeds_he"] = seeds_he
    seeds_he_list = process_he_list(hgraph, seeds_he)  #  源节点对应超边的对应 待传播节点list
    seeds_data["seeds_he_list"] = seeds_he_list
    print(seeds_data)

    data["seeds_data"] = seeds_data
    print(data)


    # =============== 处理节点领域结构的 part =================
    Algebra_data = pd.read_csv(r"C:\Users\01\Desktop\network_hyper_data\Algebra_category_data.csv", sep=',',
                               names=["he", "num"], index_col='he')
    # print(Algebra_data)
    df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 5, 10, 20, 30, 120], labels=[0, 1, 2, 3, 4]))
    # print(df_category)
    list1 = df_category.num.tolist()  # 类别个数

    category_list = []  # 定义一个新的存储分类类别的列表
    for i in range(len(set(list1))):
        category_list.append({'id': i, 'values': df_category[df_category.num == i].index.tolist()})
    print(category_list)
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
    print(list_0)
    print(list_1)
    print(list_2)
    print(list_3)
    print(list_4)


    # 分类别获取此阶段的传播节点所连接超边的待传播节点数量
    num_list = []
    for d in list_dict:
        num_1 = []
        for i in d['values']:
            num = Algebra_data.loc[i, "num"]
            num_1.append(num)
        num_list.append(sum(num_1))
    print(num_list)
    with open(r'C:\Users\01\Desktop\test.csv', "a+", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['Period', 0, 1, 2, 3, 4])
        csv_writer.writerow(["P0", num_list[0], num_list[1], num_list[2], num_list[3], num_list[4]])
        print("成功保存CSV文件……")

    # 传播路径的25步
    # propagation_path = {'P0': ['140', '66', '38'], 'P1': [], 'P2': ['4', '58', '203'], 'P3': ['303', '193', '22'], 'P4': ['216', '91'], 'P5': ['10', '94', '237', '173', '135'], 'P6': ['8', '28', '169', '163', '345', '349', '17', '154', '125'], 'P7': ['30'], 'P8': ['197', '2', '257'], 'P9': ['97', '170', '56', '74'], 'P10': ['63', '93', '318', '49', '21'], 'P11': ['183', '174', '290', '181', '322', '57'], 'P12': ['214', '230', '242', '126'], 'P13': ['248', '20', '33'], 'P14': ['201', '330', '199', '321', '31', '102'], 'P15': ['151', '147', '279', '105', '234', '143'], 'P16': ['179', '238', '157', '36', '222', '223', '184', '210'], 'P17': ['116', '243', '64', '239', '5', '167', '211'], 'P18': ['82', '176', '39', '35', '110'], 'P19': ['134', '164', '19', '60', '104', '240', '83', '23', '59', '229', '119'], 'P20': ['69', '208', '54', '191', '304', '40', '142'], 'P21': ['254', '50', '109', '71', '297', '148', '250', '123', '192'], 'P22': ['185', '120', '67', '265', '177'], 'P23': ['175', '80', '196', '85'], 'P24': ['329', '334', '215', '217']}

    #  写一个循环，得到 pie_data








