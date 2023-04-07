# -*- coding: utf-8 -*-
"""
@Time ： 2022/6/5 9:19
@Auth ： zhcj
@File ：load_vis_data.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

from src.load_index_propagation_data2 import *
from src.load_patterns_data import *
import csv

def read_hypergraph_csvs(netName):
    """
    读取超图所用到的系列数据，包括Algebra_data.csv、Algebra_category_data.csv……
    :return: hypergraph_csvs
    """
    # "D:/PyCharm2020/Trad_data/combined_signal/" + csv_name[id] + ".csv"

    with open("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + "temp_data.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        my_dict = np.load("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + netName + "_edges_to_nodes.npy", allow_pickle=True).item()
        my_dict_length = my_dict.keys()
        for key in my_dict_length:
            key_dictlist = []
            my_dict_list = my_dict[key]
            key = "E" + str(key)
            key_dictlist.append(key)
            for value in my_dict_list:
                key_dictlist.append(value)

            csv_writer.writerow(key_dictlist)

        print(netName + "_temp_data文件存储完毕！！！")

    with open("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + "temp_category_data.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        my_dict = np.load("D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/" + netName + "_edges_to_nodes.npy", allow_pickle=True).item()
        my_dict_length = my_dict.keys()
        for key in my_dict_length:
            key_dictlist = []
            my_dict_list = my_dict[key]
            key = "he" + str(key)
            key_dictlist.append(key)
            key_dictlist.append(len(my_dict_list))

            csv_writer.writerow(key_dictlist)

        print(netName + "_temp_category_data文件存储完毕！！！")

    # alg_index = read_per_node_index(netName)
    #     # alg_cluster = cluster_all_vg_node(netName)
    #     # alg_period_vg_cluster = cluster_vg_node(netName)
    #     # alg_normalization_data = read_normalized_data()
    #     # alg_pattern_data = read_patcomptor_data()
    #     # alg_data = read_algorithm_data(netName)

    return "对应hypergraph系列文件存储完毕！！！"

    return csv_writer

def read_hotmap_data():
    """
    读取每个算法的各个阶段对应的分类结果，并处理数据格式，产出完整的热力图
    :return: hotData
    """
    # alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_period_vg_cluster.npy",
    #                            allow_pickle=True).item()
    alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_period_vg_cluster.npy",
                               allow_pickle=True).item()
    # print(alg_cluster_data)

    # alg_i = "agr_1"
    # agr_data = alg_cluster_data[alg_i]
    # print(agr_data)

    cluster_list = ["period", "cluster-5", "cluster-4", "cluster-3", "cluster-2", "cluster-1"]
    hotData = {}
    agr_data = []
    for alg_i in alg_cluster_data:
        agr_i_data = []
        # period_list = []
        # period_cluster_list = []
        for period_j in alg_cluster_data[alg_i]:
            period = period_j["period"]
            # period_list.append(period)
            period_cluster = period_j["period_cluster"]
            # period_cluster_list.append(period_cluster)

        # df = pd.DataFrame(period_cluster_list, columns=cluster_list)
        # df.index = period_list
        # df.index.name = "period"
        #
        # df.to_csv("D:\PyCharm2020\PycharmProjects\hypergraph_influence\data_list\\" + alg_i + "_HMdata.csv")
            agr_i_data.append(
                {"period": period, "cluster-1": period_cluster[0], "cluster-2": period_cluster[1], "cluster-3": period_cluster[2],
                    "cluster-4": period_cluster[3], "cluster-5": period_cluster[4], "total": sum(period_cluster)})

        agr_data.append({
            "id": alg_i,
            "value": agr_i_data
        })

    hotData["data"] = agr_data
    hotData["columns"] = cluster_list

    return hotData


def read_parcoords_data(algorithm):
    """
    读取每个算法的所包含的全部节点的分类结果，并处理数据格式，产出对应的平行坐标图
    :return: parData
    """
    # 得到 算法1的系列数据
    # alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy",
    #                          allow_pickle=True).item()
    alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy",
                             allow_pickle=True).item()

    # agr_index_data = alg_index_data["agr_1"]
    agr_index_data = alg_index_data[algorithm]

    # 得到算法1的所有节点的全部 index
    period_P24 = agr_index_data[24]
    allNodes_index = period_P24["period_index"]
    # 得到算法1的分类数据
    # alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_cluster.npy",
    #                            allow_pickle=True).item()
    alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_cluster.npy",
                               allow_pickle=True).item()
    agr_cluster_data = alg_cluster_data[algorithm]
    agr_cluster_list = agr_cluster_data[0]["cluster_list"]

    # 利用allNodes_index && agr_cluster_list处理数据格式
    parData = []
    for itm in agr_cluster_list:
        id = itm["id"]
        nodes = itm["values"]
        for node in nodes:
            for vg in allNodes_index:
                if node == vg["vg_name"]:
                    parData.append(
                        {
                            "name": node,
                            "id": str(id),
                            "node_degree": vg["vg_index"][0],
                            "egonet_neighbor_degree": vg["vg_index"][1],
                            "egonet_neighbor_edges": vg["vg_index"][2],
                            "av_degree": vg["vg_index"][3],
                            "ave_alter_alter_num": vg["vg_index"][4],
                            "clustering_coefficient": vg["vg_index"][5],
                            "he_1": vg["vg_index"][6],
                            "he_2": vg["vg_index"][7],
                            "he_3": vg["vg_index"][8],
                            "he_4": vg["vg_index"][9],
                            "he_5": vg["vg_index"][10],

                        }
                    )

    return parData

def read_scatter_data(algorithm):
    """
    读取每个算法的所包含的全部节点的分类结果，并处理数据格式，产出对应的降维后的散点图
    :return:
    """
    # 得到 算法1的系列数据
    # alg_scatter_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_scatter.npy",
    #                          allow_pickle=True).item()
    alg_scatter_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_scatter.npy",
                             allow_pickle=True).item()
    agr_scatter_data = alg_scatter_data[algorithm]
    scatter_data = []
    for itm in agr_scatter_data:
        scatter_data.append({
            "id": str(itm[0]),
            "name": itm[1],
            "x": str(itm[2]),
            "y": str(itm[3])
        })
    return scatter_data

def read_covratio_data(algorithm):
    """
    计算出每个算法的每阶段的覆盖率 && 每阶段所包含的节点，并处理数据格式，产出对应的 bar+cricle 组合图
    :return: covData
    """
    # 得到超图网络的所有节点数
    # hyper_data = open('D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_data.csv')
    hyper_data = open(r'D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_data.csv')
    hyper_data = hyper_data.read()
    data = process_hypergraph(hyper_data)
    vlabel2id = data["vlabel2id"]   # algorithm 1--all nodes--423

    # 得到各阶段的节点数并计算覆盖率
    # 得到 算法1的各阶段的节点覆盖数据
    # alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy",
    #                          allow_pickle=True).item()
    alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy",
                             allow_pickle=True).item()
    # agr_index_data = alg_index_data["agr_1"]
    agr_index_data = alg_index_data[algorithm]

    covData = {}
    barData = []
    for itm in agr_index_data:
        period = itm["period"]
        index = itm["period_index"]
        cov_ratio = len(index)/len(vlabel2id)
        barData.append({
            "id": period,
            "value": cov_ratio
        })

    barData_ind = []
    source = 25
    for i in range(len(agr_index_data)):
        period = agr_index_data[i]["period"]
        index = agr_index_data[i]["period_index"]
        if i==0:
            first = index
            cov_ratio = (len(first)-source) / len(vlabel2id)
            barData_ind.append({
                "id": period,
                "value": cov_ratio
            })

        else:
            cov_ratio = (len(index) - len(agr_index_data[i-1]["period_index"])) / len(vlabel2id)
            barData_ind.append({
                "id": period,
                "value": cov_ratio
            })

    # 得到 算法1的各阶段的节点覆盖率数据
    covData["barData"] = barData
    covData["barData_ind"] = barData_ind

    return covData

def read_patcomptor_data():
    """
    计算出每个算法对应模式所包含类别各指标的平均数据，并处理数据格式，产出对应的 南丁格尔玫瑰图
    :return: patData
    """
    # alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_cluster.npy",
    #                            allow_pickle=True).item()
    # alg_normalization_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_normalization.npy",
    #                            allow_pickle=True).item()
    alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_cluster.npy",
                                allow_pickle=True).item()
    alg_normalization_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_normalization.npy",
                                     allow_pickle=True).item()

    index_name = ["node_degree", "egonet_neighboring_degree", "egonet_neighboring_edges", "average_degree",
                  "average_alter_alter_num", "clustering_coefficient", "list_0_he_list", "list_1_he_list",
                  "list_2_he_list", "list_3_he_list", "list_4_he_list"]

    color = ["#9E0041", "#C32F4B", "#E1514B", "#F47245", "#FB9F59", "#FEC574", "#FAE38C", "#EAF195", "#C7E89E", "#9CD6A4", "#6CC4A4",
             "#4D9DB4", "#4776B4", "#5E4EA1"]

    # 得到超图网络的所有节点数
    # hyper_data = open('D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_data.csv')
    hyper_data = open(r'D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_data.csv')
    hyper_data = hyper_data.read()
    data = process_hypergraph(hyper_data)
    vlabel2id = data["vlabel2id"]  # algorithm 1--all nodes--423

    patData = {}
    for alg_i in alg_normalization_data:
        agr_normalization_data = alg_normalization_data[alg_i]
        # agr_cluster_list = agr_cluster_data[0]["cluster_list"]
        agr_cluster_data = alg_cluster_data[alg_i]
        agr_cluster_list = agr_cluster_data[0]["cluster_list"]

        per_patData = []
        for itm in agr_cluster_list:
            id = itm["id"]
            nodes = itm["values"]
            cov_ratio = len(nodes) / len(vlabel2id)

            id_index_list = []
            for node in nodes:
                for vg in agr_normalization_data:
                    if node == vg["vg_name"]:
                        id_index_list.append(vg["vg_index"])

            id_index = np.array(id_index_list)
            id_index = np.mat(id_index)

            id_avg_index = np.mean(id_index, 0).tolist()[0]

            value = []
            for i in range(len(id_avg_index)):
                value.append({
                    "id": str(id),
                    "label": index_name[i],
                    "score": id_avg_index[i],
                    "color": color[i],
                    # "weight": id_avg_index[i] / sum(id_avg_index)
                    "weight": 1 / 11
                })

            per_patData.append({
                "id": str(id),
                "id_avg_index": value,
                "coverage": cov_ratio
            })
        patData[alg_i] = per_patData
    # np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_pattern" + '.npy',
    #         patData)  # 保存
    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_pattern" + '.npy',
            patData)  # 保存
    print("temp_alg_pattern文件存储完毕！！！")

    return patData

def read_pattern_data(agr_name):
    """
    处理每个算法对应模式，并处理数据格式，产出对应的 南丁格尔玫瑰图
    :return: pattern_data
    """
    # alg_pattern_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_pattern.npy",
    #                            allow_pickle=True).item()
    alg_pattern_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_pattern.npy",
                               allow_pickle=True).item()

    # patterns = {"agr_1": [["3"], ["4"], ["3", "4"]], "agr_2": [["2"], ["3"], ["2", "3"]]}
    patterns = get_patterns_data()    #######################重点关注一下#############

    # agr_pat = [["3"], ["4"], ["3", "4"]]  # 对应算法的pattern
    #
    # algorithm = "agr_1"  # 对应的算法

    algorithm = agr_name
    agr_pat = patterns[agr_name]

    agr_pattern_data = alg_pattern_data[algorithm]
    # data = agr_pattern_data[3]["id_avg_index"]

    algorithm_data = []
    pattern_data = []
    for i in range(len(agr_pat)):
        per_pattern_data = []
        pat = agr_pat[i][0]
        sup = agr_pat[i][1]

        cov_ratio = 0  # pattern累积的节点覆盖率
        for id in pat:
            id_avg_index = agr_pattern_data[int(id)]["id_avg_index"]
            coverage = agr_pattern_data[int(id)]["coverage"]
            cov_ratio +=coverage
            per_pattern_data.append({
                "id": id,
                "value": id_avg_index
            })

        pattern_data.append({
            "pattern": i,
            "value": per_pattern_data,
            "sup": str(sup),
            "coverage": cov_ratio
        })

    algorithm_data.append({
        "algorithm": algorithm,
        "value": pattern_data
    })

    return algorithm_data

# origin---read_box_data
# def read_box_data():
#     '''
#       聚类结果的五个类别的'南丁格尔图'及'盒须图'
#     :return:
#     '''
#     # 南丁格尔图
#     alg_pattern_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_pattern.npy",
#                                allow_pickle=True).item()
#     # 盒须图
#     alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_cluster.npy",
#                                allow_pickle=True).item()
#     alg_normalization_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_normalization.npy",
#                                 allow_pickle=True).item()
#
#     agr_name = 'agr_1'
#     index_name = ["node_degree", "egonet_neighboring_degree", "egonet_neighboring_edges", "average_degree",
#                   "average_alter_alter_num", "clustering_coefficient", "list_0_he_list", "list_1_he_list",
#                   "list_2_he_list", "list_3_he_list", "list_4_he_list"]
#     # 单个算法的系列数据
#     per_pattern = alg_pattern_data[agr_name]
#     per_box_group = alg_cluster_data[agr_name][0]['cluster_list']
#     per_vg_index_normalization = alg_normalization_data[agr_name]
#
#     pattern_box_group = []
#     for i in range(len(per_pattern)):  # item=0
#         id = per_pattern[i]['id']  # id
#         id_avg_index = per_pattern[i]['id_avg_index']  # pattern
#         id_cluster_data = per_box_group[i]['values']
#
#         vg_index_list = []  # 该类别的每个节点的index数组
#         for vg in id_cluster_data:
#             for vg_ind in per_vg_index_normalization:
#                 if vg == vg_ind['vg_name']:
#                     vg_index_list.append(vg_ind['vg_index'])
#
#         index_length = len(vg_index_list[0])  # index的长度
#
#         # box_data = []  # box的数据
#         # for num in range(index_length):
#         #     per_index_data = []  # 每个index的系列数据
#         #     for item in vg_index_list:
#         #         per_index_data.append(item[num])
#         #     box_data.append(per_index_data)
#
#         box_data = []  # box的数据
#         for item in vg_index_list:
#             for num in range(index_length):
#                 box_data.append({
#                     "value": int(id)+1,
#                     "y": item[num],
#                     "x": index_name[num]
#                 })
#
#         pattern_box_group.append({
#             "id": id,
#             "box_data": [box_data],
#             "value": [{
#                 "id": id,
#                 "id_avg_index": id_avg_index
#             }]
#         })
#
#     return pattern_box_group

def read_box_data():
    '''
      聚类结果的五个类别的'南丁格尔图'及'盒须图'
    :return:
    '''
    # 南丁格尔图
    # 盒须图
    all_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_all_alg_cluster.npy",
                               allow_pickle=True)
    all_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_all_alg_index.npy",
                                allow_pickle=True)

    index_name = ["node_degree", "egonet_neighboring_degree", "egonet_neighboring_edges", "average_degree",
                  "average_alter_alter_num", "clustering_coefficient", "list_0_he_list", "list_1_he_list",
                  "list_2_he_list", "list_3_he_list", "list_4_he_list"]
    color = ["#9E0041", "#C32F4B", "#E1514B", "#F47245", "#FB9F59", "#FEC574", "#FAE38C", "#EAF195", "#C7E89E",
             "#9CD6A4", "#6CC4A4",
             "#4D9DB4", "#4776B4", "#5E4EA1"]
    # 单个算法的系列数据
    per_box_group = all_cluster_data[0]['cluster_list']

    vg_name_list = []
    vg_index_list = []
    normalization_list = []  # 标准化
    for vg in all_index_data:
        vg_name_list.append(vg["vg_name"])
        vg_index_list.append(vg["vg_index"])

    vg_index0 = np.array(vg_index_list)
    vg_index1 = pd.DataFrame(vg_index0)
    vg_index1.insert(0, "vg", vg_name_list, allow_duplicates=False)
    svg_index = vg_index1.drop(['vg'], axis=1)

    points = svg_index.values
    # 将原始数据做归一化处理
    data = whiten(points).tolist()

    for vg_i in range(len(vg_name_list)):
        normalization_list.append({
            "vg_name": vg_name_list[vg_i],
            "vg_index": data[vg_i]
        })

    # 各指标的平均值，pattern小图
    per_patData = []
    for itm in per_box_group:
        id = itm["id"]
        nodes = itm["values"]

        id_index_list = []
        for node in nodes:
            for vg in normalization_list:
                if node == vg["vg_name"]:
                    id_index_list.append(vg["vg_index"])

        id_index = np.array(id_index_list)
        id_index = np.mat(id_index)

        id_avg_index = np.mean(id_index, 0).tolist()[0]

        value = []
        for i in range(len(id_avg_index)):
            value.append({
                "id": str(id),
                "label": index_name[i],
                "score": id_avg_index[i],
                "color": color[i],
                "weight": 1 / 11
            })

        per_patData.append({
            "id": str(id),
            "id_avg_index": value,
        })

    pattern_box_group = []
    for i in range(len(per_patData)):  # item=0
        id = per_patData[i]['id']  # id
        id_avg_index = per_patData[i]['id_avg_index']  # pattern
        id_cluster_data = per_box_group[i]['values']

        vg_index_list = []  # 该类别的每个节点的index数组
        for vg in id_cluster_data:
            for vg_ind in normalization_list:
                if vg == vg_ind['vg_name']:
                    vg_index_list.append(vg_ind['vg_index'])

        index_length = len(vg_index_list[0])  # index的长度

        box_data = []  # box的数据
        for item in vg_index_list:
            for num in range(index_length):
                box_data.append({
                    "value": int(id)+1,
                    "y": item[num],
                    "x": index_name[num]
                })

        pattern_box_group.append({
            "id": id,
            "box_data": [box_data],
            "value": [{
                "id": id,
                "id_avg_index": id_avg_index
            }]
        })

    return pattern_box_group



def read_normalized_data():
    """
    得到每个算法的所有节点的归一化之后的指标值，存npy文件
    :return: normalized_clustered_data
    """
    # alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy",
    #                          allow_pickle=True).item()
    alg_index_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_index.npy",
                             allow_pickle=True).item()

    per_alg_normalization = {}
    for alg_i in alg_index_data:
        normalization_list = []
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
                vg_index1 = pd.DataFrame(vg_index0)
                vg_index1.insert(0, "vg", vg_name_list, allow_duplicates=False)
                svg_index = vg_index1.drop(['vg'], axis=1)

                points = svg_index.values
                # 将原始数据做归一化处理
                data = whiten(points).tolist()

                for vg_i in range(len(vg_name_list)):
                    normalization_list.append({
                        "vg_name": vg_name_list[vg_i],
                        "vg_index": data[vg_i]
                    })

        per_alg_normalization[alg_i] = normalization_list

    # np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\alg_normalization" + '.npy', per_alg_normalization)  # 保存
    np.save("D:\PyCharm2020\PycharmProjects\hypergraph_influence\static" + "\\temp_alg_normalization" + '.npy', per_alg_normalization)  # 保存

    return per_alg_normalization

def read_variance_data():
    """
    hotmap视图的各个算法的方差，并与之分类
    :return:
    """
    alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\alg_period_vg_cluster.npy",
                               allow_pickle=True).item()
    # alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_period_vg_cluster.npy",
    #                            allow_pickle=True).item()

    varData = {}
    agr_data = []
    for alg_i in alg_cluster_data:
        var0 = []
        var1 = []
        var2 = []
        var3 = []
        var4 = []
        for period_j in alg_cluster_data[alg_i]:
            period = period_j["period"]
            period_cluster = period_j["period_cluster"]
            var0.append(period_cluster[0])
            var1.append(period_cluster[1])
            var2.append(period_cluster[2])
            var3.append(period_cluster[3])
            var4.append(period_cluster[4])

        var_sum = (np.var(np.array(var0)) + np.var(np.array(var1)) + np.var(np.array(var2)) + np.var(np.array(var3)) + np.var(np.array(var4)))/5

        varData[alg_i] = var_sum
    return varData




if __name__ == '__main__':
    # data = read_hotmap_data()
    # data = read_scatter_data()
    # data = read_parcoords_data("agr_1")
    # data = read_covratio_data("agr_1")
    # data = read_patcomptor_data()
    # data = read_pattern_data("agr_1")
    # data = read_hypergraph_csvs("Music-Rev")
    # data = read_hypergraph_csvs("Algebra")
    # data = read_variance_data()

    data = read_box_data()
    # data = read_normalized_data()
    print(data)