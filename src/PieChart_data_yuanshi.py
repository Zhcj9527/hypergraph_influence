# -*- coding: utf-8 -*-
"""
@Time ： 2022/4/10 10:06
@Auth ： zhcj
@File ：PieChart_data_yuanshi.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""


# hyper_data = open('static/hyper_top5.csv')
#     hyper_data = open('static/Algebra_data.csv')
#     hyper_data = hyper_data.read()
#     data = process_hypergraph(hyper_data)
#
#     alg_data = read_algorithm_data()  # 算法的系列数据
#
#     # ============传播=========== ## data = hgraph
#     hgraph = data["hyper_data"]
#     vlabel2id = data["vlabel2id"]
#
#     # seeds = ["1"]   # 原始传播节点
#     # 传播路径的25步    propagation_path
#
#     pie_dict = []
#     for alg in alg_data.keys():
#         seeds = alg_data[alg]["seeds"]
#
#         propagation_path = alg_data[alg]["propagation_path"]
#
#         #  写一个循环，得到 pie_data
#         pie_data = []
#         for key in propagation_path.keys():
#
#             vg_list = propagation_path[key]
#
#             seeds_propagation = load_propagation_path(seeds, vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点
#
#             seeds = seeds_propagation
#             # seeds = vg_list
#
#             seeds_data = {}
#             # seeds = ["1"]   # 原始传播节点
#             seeds_list = process_seeds(seeds, vlabel2id)  # 处理源节点对应的label
#             seeds_data["seeds_list"] = seeds_list
#             seeds_he = process_seeds_he(hgraph, seeds_list)  # 找到包含源节点对应的超边list
#             seeds_data["seeds_he"] = seeds_he
#
#             # =============== 处理节点领域结构的 part =================
#             Algebra_data = pd.read_csv("static\Algebra_category_data.csv", sep=',',  names=["he", "num"], index_col='he')
#
#             # df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 5, 10, 20, 30, 120], labels=[0, 1, 2, 3, 4]))
#             df_category = Algebra_data.apply(lambda x: pd.cut(x, [0, 2, 4, 7, 10, 120], labels=[0, 1, 2, 3, 4]))
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
#
#             # 分类别获取此阶段的传播节点所连接超边的待传播节点数量
#             num_list = []
#             for d in list_dict:
#                 num_list.append(len(d["values"]))
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
#     data["pie_dict"] = pie_dict