import numpy as np

# algorithm_data = np.load('static\Algebra_activited_nodes_bytime_dict.npy', allow_pickle=True)

## 构造一个算法的数据格式 {'agr_1':{"seeds":[], "propagation_path":[]……}}

def read_algorithm_data():
    algorithm_data = np.load('static\Algebra_activited_nodes_bytime_dict .npy', allow_pickle=True)
    alg_dict = {}  # 创建一个空的存储算法数据的字典
    # # 遍历访问的字典所有的值
    for alg in algorithm_data.item():    # agl--str
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


if __name__ == '__main__':
    alg_data = read_algorithm_data()
    print(alg_data)