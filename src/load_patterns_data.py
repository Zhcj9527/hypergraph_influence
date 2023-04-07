# -*- coding: utf-8 -*-
"""
@Time ： 2022/7/15 20:46
@Auth ： zhcj
@File ：load_patterns_data.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

import numpy as np
import pandas as pd

def get_patterns_data():
    # alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_period_vg_cluster.npy",
    #                           allow_pickle=True).item()
    alg_cluster_data = np.load(r"D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_alg_period_vg_cluster.npy",
                               allow_pickle=True).item()

    algorithm_list = list(alg_cluster_data.keys())  # 将算法的名称转变为列表

    alg_seq_data = {}
    # alg_i = "agr_8"
    for alg_i in algorithm_list:
        filter_cluster = []  #
        for period_j in alg_cluster_data[alg_i]:
            # period = period_j["period"]
            period_cluster = period_j["period_cluster"]

            def filter_0(period_cluster):
                """ 把0过滤掉，给period打上对应的分类标签 """
                filter_period_list = []
                for i in range(len(period_cluster)):
                    # if period_cluster[i] != 0:
                    if period_cluster[i] / sum(period_cluster) > 0:  # 单个数值的比例大于总数值的10%，则输出
                        filter_period_list.append(i)

                return filter_period_list

            filter_cluster.append(filter_0(period_cluster))

        # print(filter_cluster)

        # control the length of sequence
        num = 6
        list_5 = []
        length = len(filter_cluster)
        count = 0
        input_direct = []

        while length >= num:
            for i in range(length):
                count += 1
                if count == num:
                    for itm in range(num):
                        list_5.append(filter_cluster[itm])
                    # print(list_5)
                    input_direct.append(list_5)

                    filter_cluster.pop(0)  ## 删除第一个元素
                    length = len(filter_cluster)
                    count = 0
                    list_5 = []  ## 清空列表

        processed_data = handle_input(input_direct)

        # 将处理过的输入数据 按.txt文件存起来
        path = r'D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\test_files\patterns.txt'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(processed_data)
            f.close()

        patterns = parse_output(alg_i)

        df = to_pandas_dataframe(patterns)
        # 相同ID聚在一类
        df = df.groupby("pattern").sum()
        # 按照支持度排序
        df.sort_values(by='sup', axis=0, ascending=False, inplace=True)
        # 得到索引和对应的值列表
        index_list = df.index.tolist()
        value_list = df["sup"].tolist()
        # 将列表转换成Series，并合并成pattern_df
        pattern_series = pd.Series(index_list)
        sup_series = pd.Series(value_list)
        pattern_df = pd.concat([pattern_series, sup_series], axis=1, ignore_index=False)
        pattern_df.columns = ["pattern", "sup"]
        pattern_df1 = pattern_df.sort_values(by=["sup", "pattern"], axis=0, ascending=(False, True))

        # 处理成pattern所需要的格式
        patterns_list = []
        pattern_list = []
        for itm in range(len(pattern_df1)):
            pattern = pattern_df1["pattern"][itm]
            sup = pattern_df1["sup"][itm]

            pattern_list.append(list(pattern))
            pattern_list.append(sup)

            patterns_list.append(pattern_list)
            pattern_list = []

        alg_seq_data[alg_i] = patterns_list

    return alg_seq_data

def handle_input(input_direct):
    """
        处理成输入的格式
    :param input_direct:
    :return:
    """
    if type(input_direct) == list:
        seq_spmf = ""
        for seq in input_direct:
            for item_set in seq:
                for item in item_set:
                    seq_spmf += str(item) + ' '
                seq_spmf += str(-1) + ' '
            seq_spmf += str(-2) + '\n'

        return seq_spmf


def parse_output(alg_i):
    """
    Parse the output of SPMF and saves in in member variable patterns_
    -1 separates itemsets
    -2 indicates end of a sequence
    http://data-mining.philippe-fournier-viger.com/introduction-to-sequential-rule-mining/#comment-4114
    """
    lines = []

    # path = "D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/test_files/algorithm_patterns/music-pattern-6-70%-24/" + alg_i + ".txt"
    path = "D:/PyCharm2020/PycharmProjects/hypergraph_influence/static/test_files/algorithm_patterns/pattern-6-70%-24/" + alg_i + ".txt"
    # print(path)
    with open(path, "r") as f:
        lines = f.readlines()

    patterns = []
    for line in lines:
        line = line.strip()
        patterns.append(line.split(" -1 "))

    return patterns


def to_pandas_dataframe(patterns):
    """
    Convert output to pandas DataFrame
    pickle: Save as serialized pickle
    """
    # TODO: Optional parameter for pickle file name

    patterns_dict_list = []
    for pattern_sup in patterns:
        pattern = pattern_sup[:-1]
        pattern_list = []
        for itm in pattern:
            itm = itm.split(" ")
            for i in itm:
                pattern_list.extend(i)

        # 转换成字符串
        pattern_str = ""
        for itm in pattern_list:
            pattern_str += itm
        sup = pattern_sup[-1:][0]
        sup = sup.strip()
        if not sup.startswith("#SUP"):
            print("support extraction failed")
        sup = sup.split()
        sup = sup[1]

        patterns_dict_list.append({'pattern': pattern_str, 'sup': int(sup)})

        pattern_list = []

    df = pd.DataFrame(patterns_dict_list)

    return df



if __name__ == '__main__':
    data = get_patterns_data()
    print(data)