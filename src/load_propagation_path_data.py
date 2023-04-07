import pandas as pd
import numpy as np
import hypernetx as hnx
from sklearn.decomposition import PCA
import re
import networkx as nx

from src.load_index_propagation_data2 import *


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


#     #  得到不同算法, 传播路径的的系列数据 pie_dict 存储在data中调用
# def read_propagation_data():
#     hyper_data = open('D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_data.csv')
#   # hyper_data = open(r'D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_data.csv')
#     hyper_data = hyper_data.read()
#     data = process_hypergraph(hyper_data)
#
#     alg_data = read_algorithm_data()  # 算法的系列数据  tem_alg_data文件路径 注释本文件中的read_algorithm_data()   改成read_algorithm_data(netName)
#
#     # ============传播=========== ## data = hgraph
#     hgraph = data["hyper_data"]
#     vlabel2id = data["vlabel2id"]
#
#     # # seeds = ["1"]   # 原始传播节点
#     # seeds = ['101', '12', '15', '76', '32', '52', '27', '44', '121', '37', '7', '18', '29', '51', '14', '155', '136',
#     #          '55', '42', '156', '0', '130', '158', '11', '95']
#     #
#     # # seeds = ['155']
#     #
#     # # 传播路径的25步
#     # propagation_path = {'P0': ['140', '66', '38'], 'P1': [], 'P2': ['4', '58', '203'], 'P3': ['303', '193', '22'],
#     #                     'P4': ['216', '91'], 'P5': ['10', '94', '237', '173', '135'],
#     #                     'P6': ['8', '28', '169', '163', '345', '349', '17', '154', '125'], 'P7': ['30'],
#     #                     'P8': ['197', '2', '257'], 'P9': ['97', '170', '56', '74'],
#     #                     'P10': ['63', '93', '318', '49', '21'], 'P11': ['183', '174', '290', '181', '322', '57'],
#     #                     'P12': ['214', '230', '242', '126'], 'P13': ['248', '20', '33'],
#     #                     'P14': ['201', '330', '199', '321', '31', '102'],
#     #                     'P15': ['151', '147', '279', '105', '234', '143'],
#     #                     'P16': ['179', '238', '157', '36', '222', '223', '184', '210'],
#     #                     'P17': ['116', '243', '64', '239', '5', '167', '211'], 'P18': ['82', '176', '39', '35', '110'],
#     #                     'P19': ['134', '164', '19', '60', '104', '240', '83', '23', '59', '229', '119'],
#     #                     'P20': ['69', '208', '54', '191', '304', '40', '142'],
#     #                     'P21': ['254', '50', '109', '71', '297', '148', '250', '123', '192'],
#     #                     'P22': ['185', '120', '67', '265', '177'], 'P23': ['175', '80', '196', '85'],
#     #                     'P24': ['329', '334', '215', '217']}
#
#     pie_dict = []
#     vec_data = []
#     for alg in alg_data.keys():
#
#         seeds = alg_data[alg]["seeds"]
#
#         propagation_path = alg_data[alg]["propagation_path"]
#
#         #  写一个循环，得到 pie_data
#         pie_data = []
#         agr_vec_data = []
#         for key in propagation_path.keys():
#
#             vg_list = propagation_path[key]
#
#             # seeds_propagation = load_propagation_path(seeds, vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
#             # seeds = seeds_propagation
#
#             seeds = vg_list
#
#             seeds_data = {}
#             # seeds = ["1"]   # 原始传播节点
#             seeds_list = process_seeds(seeds, vlabel2id)  # 处理源节点对应的label
#             seeds_data["seeds_list"] = seeds_list
#             seeds_he = process_seeds_he(hgraph, seeds_list)  # 找到包含源节点对应的超边list
#
#             seeds_data["seeds_he"] = seeds_he
#             # seeds_he_list = process_he_list(hgraph, seeds_he)  #  源节点对应超边的对应 待传播节点list
#             # seeds_data["seeds_he_list"] = seeds_he_list
#             # print(seeds_data)
#
#             data["seeds_data"] = seeds_data
#             # print(data)
#
#             # =============== 处理节点领域结构的 part =================
#             Algebra_data = pd.read_csv( "D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_category_data.csv" , sep=',', names=["he", "num"], index_col='he')
#             # print(Algebra_data)
#             # Algebra_data = pd.read_csv(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_category_data.csv", sep=',', names=["he", "num"], index_col='he')
#             df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 2, 4, 7, 10, 120], labels=[0, 1, 2, 3, 4]))
#             # print(df_category)
#             list1 = df_category.num.tolist()  # 类别个数
#
#             category_list = []  # 定义一个新的存储分类类别的列表
#             for i in range(len(set(list1))):
#                 category_list.append({'id': i, 'values': df_category[df_category.num == i].index.tolist()})
#             # print(category_list)
#             # 定义分五类的列表
#             list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
#             for obj in category_list:
#                 if obj["id"] == 0:
#                     for itm in seeds_he:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
#                         if itm in obj["values"]:
#                             list_0.append(itm)
#                 elif obj["id"] == 1:
#                     for itm in seeds_he:
#                         if itm in obj["values"]:
#                             list_1.append(itm)
#                 elif obj["id"] == 2:
#                     for itm in seeds_he:
#                         if itm in obj["values"]:
#                             list_2.append(itm)
#                 elif obj["id"] == 3:
#                     for itm in seeds_he:
#                         if itm in obj["values"]:
#                             list_3.append(itm)
#                 else:
#                     for itm in seeds_he:
#                         if itm in obj["values"]:
#                             list_4.append(itm)
#
#             #  此阶段的分类别的超边列表构成的字典，形式类似 category_list
#             list_dict = [{'id': 0, 'values': list_0}, {'id': 1, 'values': list_1}, {'id': 2, 'values': list_2},
#                          {'id': 3, 'values': list_3}, {'id': 4, 'values': list_4}]
#             # print(list_dict)
#             # print(list_0)
#             # print(list_1)
#             # print(list_2)
#             # print(list_3)
#             # print(list_4)
#
#             # 分类别获取此阶段的传播节点所连接超边的待传播节点数量
#             num_list = []
#             for d in list_dict:
#                 num_list.append(len(d["values"]))
#
#             agr_vec_data.append(num_list)
#             # print(num_list)
#
#                 # num_1 = []
#                 # for i in d['values']:
#                 #     num = Algebra_data.loc[i, "num"]
#                 #     num_1.append(num)
#                 # num_list.append(sum(num_1))
#             # print(num_list)
#
#             # with open(r'C:\Users\01\Desktop\test.csv', "a+", newline="") as csv_file:
#             #     csv_writer = csv.writer(csv_file, delimiter=',')
#             #     csv_writer.writerow(['Period', 0, 1, 2, 3, 4])
#             #     csv_writer.writerow(["P0", num_list[0], num_list[1], num_list[2], num_list[3], num_list[4]])
#             #     print("成功保存CSV文件……")
#
#             pie_data.append({
#                 "period": key,
#                 "sum": str(sum(num_list)),
#                 "category_num": list(set(list1)),
#                 "category_list":
#                     [{'id': str(0), 'values': str(num_list[0])}, {'id': str(1), 'values': str(num_list[1])},
#                      {'id': str(2), 'values': str(num_list[2])},
#                      {'id': str(3), 'values': str(num_list[3])}, {'id': str(4), 'values': str(num_list[4])}],
#                 "vg_list": vg_list,
#                 "category": category_list,
#                 "algorithm": alg
#             })
#         pie_dict.append({"name": alg, "values": pie_data})
#
#         vec_data.append({"name": alg, "vector": agr_vec_data})
#
#     # data["pie_data"] = pie_data
#     data["pie_dict"] = pie_dict
#     data["vec_data"] = vec_data
#
#     return data

    ## 构造一个算法的数据格式 {'agr_1':{"seeds":[], "propagation_path":[]……}}
def read_algorithm_data():
    algorithm_data = np.load('D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\Algebra_activited_nodes_bytime_dict .npy', allow_pickle=True)
    alg_dict = {}  # 创建一个空的存储算法数据的字典
    # # 遍历访问的字典所有的值
    for alg in algorithm_data.item():  # agl--str
        ## 源节点的处理 ，访问到 seed_num_info
        alg_data = algorithm_data.item()[alg]
        seed_num_info = alg_data[0]["seed_num_info"]
        seeds = seed_num_info["seeds"]
        ## 处理成需要的结果
        seed_list = []  ## 源节点的格式
        for seed in seeds:
            seed = str(seed)
            seed_list.append(seed)

        ## 传播路径的处理
        seed_num_info = alg_data[0]["seed_num_info"]
        mydict_length = seed_num_info["activated_seeds_bytime"].keys()
        mydict = {}  ## 传播路径的格式
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


    #  获得对应 pie period-algorithm-selected 的具体节点的 node_pie_data
def read_nodes_data(algorithm):
    propagation_data = read_propagation_data()     # 得到传播数据 以及对应的算法集数据
    hgraph = propagation_data["hyper_data"]
    vlabel2id = propagation_data["vlabel2id"]
    pie_dict = propagation_data["pie_dict"]

    category_list = pie_dict[0]["values"][0]["category"]
    category_num = pie_dict[0]["values"][0]["category_num"]

    alg_normalization_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_normalization.npy",
                                    allow_pickle=True).item()

    index_name = ["node_degree", "egonet_neighboring_degree", "egonet_neighboring_edges", "average_degree",
                  "average_alter_alter_num", "clustering_coefficient", "list_0_he_list", "list_1_he_list",
                  "list_2_he_list", "list_3_he_list", "list_4_he_list"]

    color = ["#9E0041", "#C32F4B", "#E1514B", "#F47245", "#FB9F59", "#FEC574", "#FAE38C", "#EAF195", "#C7E89E",
             "#9CD6A4", "#6CC4A4", "#4D9DB4", "#4776B4", "#5E4EA1"]

    for itm0 in pie_dict:
        if itm0["name"] == algorithm:
            agr_normalization_data = alg_normalization_data[algorithm]
            # 一个算法对应的 每一阶段的 vg_list 的values
            nodes_pie_dict_arr = []
            for itm1 in itm0["values"]:

                vg_list = itm1["vg_list"]

                # 对每一个node进行遍历
                node_pie_data = []
                for vg in vg_list:

                    # seeds = vg  # 源节点

                    vg_label = vlabel2id[vg]  # 处理源节点对应的label

                    seeds_he_list = []
                    for i in hgraph["links"]:
                        if i["target"] == vg_label:
                            seeds_he_list.append(i["source"])

                    # 定义分五类的列表
                    list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
                    for obj in category_list:
                        if obj["id"] == 0:
                            for itm in seeds_he_list:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
                                if itm in obj["values"]:
                                    list_0.append(itm)
                        elif obj["id"] == 1:
                            for itm in seeds_he_list:
                                if itm in obj["values"]:
                                    list_1.append(itm)
                        elif obj["id"] == 2:
                            for itm in seeds_he_list:
                                if itm in obj["values"]:
                                    list_2.append(itm)
                        elif obj["id"] == 3:
                            for itm in seeds_he_list:
                                if itm in obj["values"]:
                                    list_3.append(itm)
                        else:
                            for itm in seeds_he_list:
                                if itm in obj["values"]:
                                    list_4.append(itm)

                    #  这个过程把对应节点的index数据提取到
                    id_index_list = []
                    for node in agr_normalization_data:
                        if vg == node["vg_name"]:
                            id_index_list.append(node["vg_index"])

                    value = []
                    for i in range(len(id_index_list[0])):
                        value.append({
                            "label": index_name[i],
                            "values": id_index_list[0][i],
                            "color": color[i],
                        })


                    #  此阶段的分类别的超边列表构成的字典，形式类似 category_list
                    list_dict = [{'id': 0, 'values': list_0}, {'id': 1, 'values': list_1},
                                 {'id': 2, 'values': list_2},
                                 {'id': 3, 'values': list_3}, {'id': 4, 'values': list_4}]

                    # 分类别获取此阶段的传播节点所连接超边的待传播节点数量
                    num_list = []
                    for d in list_dict:
                        num_list.append(len(d["values"]))

                    # 各个结构指标可以放在这里

                    node_pie_data.append({
                        "node": vg,
                        "sum": sum(num_list),
                        "category_num": index_name,
                        "category_list": value,
                        "vg_list": vg_list,
                        "category": category_list
                    })
                ## 按照超边数量大小进行排序
                ordered_list = sorted(node_pie_data, key=lambda vg: vg['sum'], reverse=True)
                new_ordlist = list(filter(lambda x : x['sum'] > 5, ordered_list))
                for item in range(len(new_ordlist)):
                    new_ordlist[item]['sum'] = str(new_ordlist[item]['sum'])

                nodes_pie_dict_arr.append({"name": algorithm, "period": itm1["period"], "values": new_ordlist})

    return nodes_pie_dict_arr

 #  获得对应 pie period-algorithm-selected 的具体节点的 node_pie_data --->>>  'origin'
# def read_nodes_data(algorithm):
#     propagation_data = read_propagation_data()     # 得到传播数据 以及对应的算法集数据
#     hgraph = propagation_data["hyper_data"]
#     vlabel2id = propagation_data["vlabel2id"]
#     pie_dict = propagation_data["pie_dict"]
#
#     category_list = pie_dict[0]["values"][0]["category"]
#     category_num = pie_dict[0]["values"][0]["category_num"]
#
#     for itm0 in pie_dict:
#         if itm0["name"] == algorithm:
#             # 一个算法对应的 每一阶段的 vg_list 的values
#             nodes_pie_dict_arr = []
#             for itm1 in itm0["values"]:
#
#                 vg_list = itm1["vg_list"]
#
#                 # 对每一个node进行遍历
#                 node_pie_data = []
#                 for vg in vg_list:
#
#                     # seeds = vg  # 源节点
#
#                     vg_label = vlabel2id[vg]  # 处理源节点对应的label
#
#                     seeds_he_list = []
#                     for i in hgraph["links"]:
#                         if i["target"] == vg_label:
#                             seeds_he_list.append(i["source"])
#
#                     # 定义分五类的列表
#                     list_0, list_1, list_2, list_3, list_4 = [], [], [], [], []
#                     for obj in category_list:
#                         if obj["id"] == 0:
#                             for itm in seeds_he_list:  # 从此时的seeds_he中获取此阶段的超边列表，从而获取此阶段的节点所连接超边的待传播节点数量
#                                 if itm in obj["values"]:
#                                     list_0.append(itm)
#                         elif obj["id"] == 1:
#                             for itm in seeds_he_list:
#                                 if itm in obj["values"]:
#                                     list_1.append(itm)
#                         elif obj["id"] == 2:
#                             for itm in seeds_he_list:
#                                 if itm in obj["values"]:
#                                     list_2.append(itm)
#                         elif obj["id"] == 3:
#                             for itm in seeds_he_list:
#                                 if itm in obj["values"]:
#                                     list_3.append(itm)
#                         else:
#                             for itm in seeds_he_list:
#                                 if itm in obj["values"]:
#                                     list_4.append(itm)
#
#                     #  此阶段的分类别的超边列表构成的字典，形式类似 category_list
#                     list_dict = [{'id': 0, 'values': list_0}, {'id': 1, 'values': list_1},
#                                  {'id': 2, 'values': list_2},
#                                  {'id': 3, 'values': list_3}, {'id': 4, 'values': list_4}]
#
#                     # 分类别获取此阶段的传播节点所连接超边的待传播节点数量
#                     num_list = []
#                     for d in list_dict:
#                         num_list.append(len(d["values"]))
#
#                     # 各个结构指标可以放在这里
#
#                     node_pie_data.append({
#                         "node": vg,
#                         "sum": str(sum(num_list)),
#                         "category_num": category_num,
#                         "category_list":
#                             [{'id': str(0), 'values': str(num_list[0])}, {'id': str(1), 'values': str(num_list[1])},
#                              {'id': str(2), 'values': str(num_list[2])},
#                              {'id': str(3), 'values': str(num_list[3])},
#                              {'id': str(4), 'values': str(num_list[4])}],
#                         "vg_list": vg_list,
#                         "category": category_list
#                     })
#
#                 nodes_pie_dict_arr.append({"name": algorithm, "period": itm1["period"], "values": node_pie_data})
#
#     return nodes_pie_dict_arr

def read_agr_reduceDim_data():
    data = read_propagation_data()
    vec_data = data["vec_data"]
    period_arr = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16',
                'P17', 'P18', 'P19', 'P20', 'P21', 'P22', 'P23', 'P24']


    #  得到降维的数据——折线呈现
    points = []
    values = []
    #  把得到的折线聚类以发现共同模式,先得到聚类的数据框然后在k-means聚类——dic
    dic = {}
    for agr_id in vec_data:
        agr_name = agr_id["name"]
        agr_vec = agr_id["vector"]

        X = np.array(agr_vec)
        pca = PCA(n_components=1, copy=True, whiten=False)  # 降到一维
        pca.fit(X)  # train
        newX = pca.fit_transform(X).reshape((1, 25)).tolist()

        dic[agr_name] = newX[0]

        results = [list(item) for item in zip(period_arr, newX[0])]  # 转换成一个以列表构成的列表

        for result in results:
            values.append({'name': str(result[0]), 'value': float(result[1])})
        points.append({'id': agr_name, 'values': values})
        values = []

    cluster_df0 = pd.DataFrame(dic)
    cluster_df1 = cluster_df0.T
    cluster_df1.columns = period_arr
    cluster_df1.index.name = "algorithm"
    cluster_df1.to_csv(r"C:\Users\01\Desktop\rd.csv")

    return points
        # print(pca.explained_variance_ratio_)  # 输出贡献率
        # print(newX)

    # 得到各个算法序列的 dis/sim
def read_algorithm_dis_data():

    data = read_propagation_data()
    vec_data = data["vec_data"]

    alg_dis_list = []
    for i in range(len(vec_data)-1):
        agr_i = vec_data[i]
        for j in range(i+1, len(vec_data)):
            agr_j = vec_data[j]

            i_arr = agr_i["vector"]
            j_arr = agr_j["vector"]

            dis_list = []
            for itm in range(len(i_arr)):
                i_vec = np.array(i_arr[itm])
                j_vec = np.array(j_arr[itm])

                dis = np.linalg.norm(i_vec-j_vec, ord=2)
                # dis2 = np.sqrt(sum((i_vec-j_vec) ** 2))
                dis_list.append(dis)

            alg_dis = np.mean(dis_list)

            alg_dis_list.append({
                # "id": "agr_" + str(i+1) + "->" + "agr_" + str(j+1),
                "id":  str(i + 1) + "->" + str(j + 1),
                "value": alg_dis
            })

    return alg_dis_list

# # 获取每对（，）的 dis
# def read_per_agrs_dis(agr1, agr2):
#     i_arr = agr1["vector"]
#     j_arr = agr2["vector"]
#
#     dis_list = []
#     for itm in range(len(i_arr)):
#         i_vec = np.array(i_arr[itm])
#         j_vec = np.array(j_arr[itm])
#
#         dis = np.linalg.norm(i_vec, j_vec)
#         dis_list.append(dis)
#
#     return np.mean(dis_list)


if __name__ == '__main__':
    nodes_data = read_nodes_data("agr_1")
    # print(nodes_data)
    # reduceDim_data = read_agr_reduceDim_data()
    # dis = read_algorithm_dis_data()
    # data = read_propagation_data()

    print(data)










