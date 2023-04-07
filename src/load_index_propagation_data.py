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
def read_algorithm_data():
    algorithm_data = np.load('D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_activited_nodes_bytime_dict .npy', allow_pickle=True)
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

    return alg_dict


def read_per_node_index():
    hyper_data = open('D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_data.csv')
    hyper_data = hyper_data.read()
    data = process_hypergraph(hyper_data)

    alg_data = read_algorithm_data()  # 每个算法的系列数据
    hgraph = data["hyper_data"]
    vlabel2id = data["vlabel2id"]

    # 超边分类的数据
    Algebra_data = pd.read_csv("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_category_data.csv",
                               sep=',',
                               names=["he", "num"], index_col='he')
    # df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 7, 120], labels=[0, 1]))
    df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 2, 4, 7, 10, 120], labels=[0, 1, 2, 3, 4]))
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
    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_index" + '.npy', per_alg_index_data)  # 保存

    return per_alg_index_data

def cluster_all_vg_node():
    """"
        得到每个算法的全部节点的分类结果
    """
    alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\alg_index.npy", allow_pickle=True).item()
    per_alg_cluster = {}
    per_alg_scatter = {}
    for alg_i in alg_index_data:
        period_cluster_list = []
        scatters = []
        for period_j in alg_index_data[alg_i]:
            if period_j["period"] == "P24":
                period = period_j["period"]
                period_index = period_j["period_index"]
                vg_name_list = []
                vg_index_list = []
                for vg in period_index:
                    vg_name_list.append(vg["vg_name"])
                    vg_index_list.append(vg["vg_index"])

                vg_index0 = np.array(vg_index_list)
                # # 数据降维(4)
                # pca = PCA(n_components=4, copy=True, whiten=False)  # 降到四维
                # pca.fit(vg_index0)  # train
                # newX = pca.fit_transform(vg_index0)
                # vg_index1 = pd.DataFrame(newX)
                vg_index1 = pd.DataFrame(vg_index0)
                vg_index1.insert(0, "vg", vg_name_list, allow_duplicates=False)
                # vg_index1.to_csv(r"C:\Users\01\Desktop\rd_index.csv")

                # # 数据规整化处理及k-means聚类
                svg_index = vg_index1.drop(['vg'], axis=1)
                # # svg_index_scaled = preprocessing.scale(svg_index) # 数据规整化处理
                # #
                # # myKmeans = KMeans(algorithm='auto', n_clusters=5, n_init=10, max_iter=200)
                # # myKmeans.fit(svg_index_scaled)
                # # vg_cluster_result = myKmeans.predict(svg_index).tolist()

                points = svg_index.values
                # 将原始数据做归一化处理
                data = whiten(points)


                centroid = kmeans(data, 5)[0]  # 分为5类
                print(centroid)  # 输出中心
                # 使用vq函数根据聚类中心对所有数据进行分类,vq的输出也是两维的,[0]表示的是所有数据的label
                label = vq(data, centroid)[0]
                print(label)

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

                scatter = []
                for i in range(len(scatters1)):
                    scatter.append(scatters1[i][0])
                    scatter.append(scatters1[i][1])
                    scatter.append(scatters2[i][0])
                    scatter.append(scatters2[i][1])
                    scatters.append(scatter)
                    scatter = []


                print(data_tsne)
                #
                # # 根据类别分割数据后，画图
                # d = data_tsne[data_tsne.index == 0]  # 找出聚类类别为0的数据对应的降维结果
                # plt.scatter(d[0], d[1], c='lightgreen', marker='o')
                # d = data_tsne[data_tsne.index == 1]
                # plt.scatter(d[0], d[1], c='orange', marker='o')
                # d = data_tsne[data_tsne.index == 2]
                # plt.scatter(d[0], d[1], c='lightblue', marker='o')
                # d = data_tsne[data_tsne.index == 3]
                # plt.scatter(d[0], d[1], c='green', marker='o')
                # d = data_tsne[data_tsne.index == 4]
                # plt.scatter(d[0], d[1], c='blue', marker='o')
                # d = data_tsne[data_tsne.index == 5]
                # plt.scatter(d[0], d[1], c='red', marker='o')
                # d = data_tsne[data_tsne.index == 6]
                # plt.scatter(d[0], d[1], c='black', marker='o')
                # plt.show()

                warnings.filterwarnings("ignore")
                # warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=793)

                results = [list(item) for item in zip(label, vg_name_list)]  # 转换成一个以列表构成的列表

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

                # _num = [{'id': str(0), 'values': len(list_0)}, {'id': str(1), 'values': len(list_1)},
                #         {'id': str(2), 'values': len(list_2)}, {'id': str(3), 'values': len(list_3)},
                #         {'id': str(4), 'values': len(list_4)}]

                # #  结果输出
                # def print_kmcluster(k):
                #     '''用于聚类结果的输出k：为聚类中心个数'''
                #     for i in range(k):
                #         print('聚类', i)
                #         ls = []
                #         for index, value in enumerate(vg_cluster_result):
                #             if i == value:
                #                 ls.append(index)
                #         print(vg_index1.loc[ls, ['vg', '0', '5', '8']])
                #
                # print_kmcluster(5)

                period_cluster_list.append({
                    "period": period,
                    "period_cluster": vg_cluster_num,
                    "cluster_list": [{'id': str(0), 'values': list_0}, {'id': str(1), 'values': list_1},
                        {'id': str(2), 'values': list_2}, {'id': str(3), 'values': list_3},
                        {'id': str(4), 'values': list_4}]
                })

        per_alg_cluster[alg_i] = period_cluster_list
        per_alg_scatter[alg_i] = scatters

    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_cluster" + '.npy', per_alg_cluster)  # 保存
    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_scatter" + '.npy', per_alg_scatter)  # 保存

    return per_alg_cluster

def cluster_vg_node():
    """
        得到每个算法每个阶段的聚类结果
    """
    alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\alg_cluster.npy",
                               allow_pickle=True).item()
    alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\alg_index.npy",
                             allow_pickle=True).item()
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

    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_period_vg_cluster" + '.npy',
            per_period_cluster)  # 保存

    return per_period_cluster

def generate_seq():
    """
        To generate the sequence
    """
    alg_cluster_data = np.load(r"/static/temp_alg_period_vg_cluster.npy", allow_pickle=True).item()

    algorithm_list = list(alg_cluster_data.keys())  # 将算法的名称转变为列表

    alg_seq_data = {}
    alg_i = "agr_1"
    # for alg_i in algorithm_list:
    filter_cluster = []
    for period_j in alg_cluster_data[alg_i]:
        # period = period_j["period"]
        period_cluster = period_j["period_cluster"]

        def filter_0(period_cluster):
            """ 把0过滤掉，给period打上对应的分类标签 """
            filter_period_list = []
            for i in range(len(period_cluster)):
                # if period_cluster[i] != 0:
                if period_cluster[i]/sum(period_cluster) > 0.18:  # 单个数值的比例大于总数值的10%，则输出
                    filter_period_list.append(i)

            return filter_period_list

        filter_cluster.append(filter_0(period_cluster))

    fn = lambda x, code='|': reduce(lambda x, y: [str(i) + code + str(j) for i in x for j in y], x)
    '''输入多个列表组成的列表, 输出其中每个列表所有元素可能的所有排列组合 code 用于分隔每个元素'''

    result = fn(filter_cluster, ",")
    seq_list = []
    for str_i in result:
        seq = str_i.strip().split(",")  # 以“ ， ”分割开，返回一个字符串列表
        # intSeq = list(map(int, seq))  # 把对应的 seq 中所有的字符串类型转换成 整型列表
        # seq_list.append(intSeq)
        seq_list.append(seq)
    F = apriori(seq_list, 0)
    print('\nfrequent itemset:\n', F)
    alg_seq_data[alg_i] = F

    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_seq" + '.npy', alg_seq_data)  # 保存

    return alg_seq_data
    # return seq_list


#  MDL算法的部分代码
def find_lcs(str1, str2):
    """"最长公共子串为：",lcs"""
    lcs = []
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    for i in range(len(str1), 0, -1):
        flag = False
        for j in range(len(str1) - i + 1):
            s = str1[j:i + j]
            #             print("第{}轮：子串长度为{}，查找str1子串 {}，查找结果(是否在str2中):".format(len(str1)-i+1,i,s),end="")
            if str2.find(s) > -1:
                lcs.append(s)
                flag = True
        if flag:
            break
    return lcs

def MinDL():
    # filter_cluster = [[0, 1], [3], [5], [0], [3], [5], [2], [2, 1], [3], [4, 2], [1]]
    filter_cluster = [[4], [4], [4], [4], [2, 4], [1, 4], [1, 4], [1, 4], [1, 4], [2], [2], [2], [2]]
    fn = lambda x, code='|': reduce(lambda x, y: [str(i) + code + str(j) for i in x for j in y], x)
    result = fn(filter_cluster, ",")  # len=64
    seq_list = []
    for str_i in result:
        seq = str_i.strip().replace(",", "")  # 以“ ， ”分割开，返回一个字符串列表
        seq_list.append(seq)

    # seq_1 = []
    # for i in range(len(seq_list) - 1):
    #     for j in range(i + 1, len(seq_list)):
    #         s1 = seq_list[i]
    #         s2 = seq_list[j]
    #         LCS = find_lcs(s1, s2)
    #         #         seq_1.append(LCS) # len -> 2016
    #         for itm in LCS:
    #             seq_1.append(itm)
    # # seq_1  # 03503522341 前两个的最大公共子字符串
    Q = []
    for i in range(len(seq_list) - 1):
        for j in range(i + 1, len(seq_list)):
            s1 = seq_list[i]
            s2 = seq_list[j]
            tuple1 = Merge(s1, s2, seq_list)
            print(tuple1)

            L0, P0 = tuple1[0], tuple1[1]
            if L0 >0:
                Q.append([L0, P0, s1, s2])

    while len(Q) != 0:
        L_list = []  # 得到带有最大值的 itm
        for itm in Q:
            L_list.append(itm[0])
        maxL = max(L_list)
        for itm in Q:
            if itm[0] == maxL:
                target_itm = itm

        c_new = target_itm[1]

        for i in [2, 3]:
            if target_itm[i] in seq_list:
                seq_list.remove(target_itm[i])
            else:pass
        seq_list.append(c_new)

        for itm in Q:
            if (target_itm[2] in itm) or (target_itm[3] in itm):
                Q.remove(itm)

        seq_list.remove(c_new)
        # 判断一下seq_list是否只有c_new,只有则输出
        if len(seq_list) != 0:
            for c in seq_list:
                L0, P0 = Merge(c, c_new, seq_list)
                if L0 > 0:
                    Q.append([L0, P0, c, c_new])
        else:
            seq_list.append(c_new)


    #
    #         print(tuple1)
    #         # print(len(tuple1[1]))
    #         count.append(tuple1)
    # print(tuple1)

    # s1 = seq_list[0]  # 03503522341234522341
    # s2 = seq_list[10]
    # tuple1 = Merge(s1, s2, seq_list)
    # print(tuple1)

    return seq_list

def Merge(s1, s2, seq_list):
    P0 = find_lcs(s1, s2)
    L0 = -1
    alpha = 1
    C = 0
    for itm in P0:
        # 得到原序列出去LCS的剩下的元素
        s1_rem = s1.replace(itm, "")
        s2_rem = s2.replace(itm, "")
        Ec = s1_rem + s2_rem

        # 遍历Ec, 计算MDL的阈值 deta L
        for str_i in Ec:  # i str
            P = itm + str_i

            def get_cost(S, P):
                sum = 0
                for s in S:
                    sum += Levenshtein.distance(s, P)
                return sum

            L1 = len(s1) + len(s2) - len(P) + alpha * get_cost(seq_list, s1) + alpha * get_cost(seq_list, s2) \
                 - alpha * get_cost(seq_list, P) + C
            # print(L1)
            if L1 < 0 or L1 < L0:
                break
            else:
                L0 = L1
                P0 = itm

    return L0, P0


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
    # data = MinDL()
    # data = generate_seq()
    # data = cluster_vg_node()
    data = cluster_all_vg_node()
    # data = read_per_node_index()

    print(data)

    # D = [["1", "3", "5"], ["2", "3", "5"], ["1", "2", "3", "5"], ["2", "5"], ["1", "2", "5"]]
    # F = apriori(D, 0.9)
    # print('\nfrequent itemset:\n', F)