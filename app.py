from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask import request
import json

# 数据处理的py文件

from src.load_line_data import *
# from src.load_hgraph_data import *
from src.load_propagation_path_data import *
from src.load_vis_data import *

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

########## 前后端交互的代码 ###################

@app.route('/get_data', methods=['GET', 'POST'])  # 前端请求后台的函数名
def get_data():
    data = read_data()
    return jsonify(data)


@app.route('/get_hgraph_data', methods=['GET', 'POST'])  # 前端请求后台的函数名
def get_hgraph_data():
    # hyper_data = open('static/hyper_top5.csv')
    # hyper_data = open('static/Algebra_data.csv')
    hyper_data = open(r'D:\PyCharm2020\PycharmProjects\hypergraph_influence\static\temp_data.csv')
    hyper_data = hyper_data.read()
    data = process_hypergraph(hyper_data)

    # ============传播=========== ## data = hgraph
    hgraph = data["hyper_data"]
    vlabel2id = data["vlabel2id"]

    # seeds = ["1"]  # 原始传播节点
    # seeds = ['155']

    post_data = request.get_json()  # 获取数据
    print("get_structure_data start...")
    seeds = post_data
    # seeds = ['101', '12', '15', '76', '32', '52', '27', '44', '121', '37', '7', '18', '29', '51', '14', '155', '136', '55', '42', '156', '0', '130', '158', '11', '95']

    # vg_list = ['11', '28']  # 传播路径对应的节点 第一阶段
    # vg_list = ['12','21','37']  # 传播路径对应的节点 第二阶段

    # vg_list = ['140', '66', '38']  # 传播路径对应的节点 第一阶段
    # vg_list = ['4', '58', '203']  # 传播路径对应的节点 第二阶段
    # seeds_propagation = load_propagation_path(seeds, vg_list)  # 传播路径对应的 v_list，加入源节点 seeds 中充当源节点

    # seeds = seeds_propagation

    seeds_data = {}
    seeds_list = process_seeds(seeds, vlabel2id)  # 处理源节点对应的label
    seeds_data["seeds_list"] = seeds_list
    seeds_he = process_seeds_he(hgraph, seeds_list)  # 找到包含源节点对应的超边list
    seeds_data["seeds_he"] = seeds_he
    seeds_he_list = process_he_list(hgraph, seeds_he)  # 源节点对应超边的对应 待传播节点list
    seeds_data["seeds_he_list"] = seeds_he_list

    data["seeds_data"] = seeds_data

    return jsonify(data)

# @app.route('/get_pie_data', methods=['GET', 'POST'])  # 前端请求后台的函数名
# def get_pie_data():
#     data = read_propagation_data()
#     return jsonify(data)

# @app.route('/get_nodes_data', methods=['GET','POST'])  # 前端请求后台的函数名
# def get_nodes_data():
#     post_data = request.get_json()  # 获取数据
#     print("get_nodes_data start...")
#     detailed_nodes_data_list = []
#     for itm in post_data:
#         algorithm = itm["algorithm"]
#         # period = itm["period"]
#
#         nodes_data = read_nodes_data(algorithm)  # 得到对应点 的嵌套数据
#
#         detailed_nodes_data_list.append({
#             "name": algorithm,
#             # "period": period,
#             "values": nodes_data
#         })
#     print("get_nodes_data done...")
#     return jsonify(detailed_nodes_data_list)

# # 1D 多折线图
# @app.route('/get_ETF_data', methods=['GET','POST'])##前端请求后台的函数名
# def get_ETF_data():
#     data = read_agr_reduceDim_data()
#     return jsonify(data)
#
# # sim 柱形图
# ########## 前后端交互的代码 ###################
# @app.route('/get_BarChart_data', methods=['GET','POST'])##前端请求后台的函数名
# def get_BarChart_data():
#     data = read_algorithm_dis_data()
#     return jsonify(data)

########## 前后端交互的代码 ###################
@app.route('/get_hotmap_data', methods=['GET','POST'])##前端请求后台的函数名
def get_hotmap_data():
    # post_data = request.get_json()  # 获取数据
    # print("get_dataset_data start...")
    # netName = post_data
    #
    # hypergraph_csvs = read_hypergraph_csvs(netName)
    #
    # print("get_hotmap_data start...")
    data = read_hotmap_data()
    return jsonify(data)

@app.route('/get_parcoords_data', methods=['GET','POST'])##前端请求后台的函数名
def get_parcoords_data():
    post_data = request.get_json()  # 获取数据
    print("get_parcoords_data start...")
    algorithm = post_data

    data = read_parcoords_data(algorithm)
    return jsonify(data)

@app.route('/get_scatter_data', methods=['GET','POST'])##前端请求后台的函数名
def get_scatter_data():
    post_data = request.get_json()  # 获取数据
    print("get_scatter_data start...")
    algorithm = post_data

    # data = read_parcoords_data(algorithm)
    data = read_scatter_data(algorithm)
    return jsonify(data)

@app.route('/get_covratio_data', methods=['GET','POST'])##前端请求后台的函数名
def get_covratio_data():
    post_data = request.get_json()  # 获取数据
    print("get_Cov_data start...")
    algorithm = post_data

    data = read_covratio_data(algorithm)
    print(data)
    # 把各阶段的细节节点数据加入进来
    detailed_nodes_data_list = []
    # algorithm = "agr_1"

    nodes_data = read_nodes_data(algorithm)  # 得到对应点 的嵌套数据
    detailed_nodes_data_list.append({
        "name": algorithm,
        "values": nodes_data
    })

    data["nodesData"] = detailed_nodes_data_list
    return jsonify(data)

@app.route('/get_patcomptor_data', methods=['GET','POST'])##前端请求后台的函数名
def get_patcomptor_data():
    post_data = request.get_json()  # 获取数据
    print("get_pattern_data start...")
    agr_name = post_data

    data = read_pattern_data(agr_name)
    return jsonify(data)

@app.route('/get_patcomptor_data2', methods=['GET','POST'])##前端请求后台的函数名
def get_patcomptor_data2():
    post_data = request.get_json()  # 获取数据
    print("get_pattern2_data start...")
    agr_name = post_data

    data = read_pattern_data(agr_name)
    return jsonify(data)

@app.route('/get_box_data', methods=['GET','POST'])##前端请求后台的函数名
def get_box_data():
    data = read_box_data()
    return jsonify(data)

# ########## 前后端交互的代码 ###################
# @app.route('/get_HorizonBar_data', methods=['GET','POST'])##前端请求后台的函数名
# def get_HorizonBar_data():
#     data = [{"name": "data_left", "value": [{"name": "Locke", "value": 4, "coverage": 0.13}, {"name": "Reyes", "value": 15, "coverage": 0.26}, {"name": "Ford", "value": 23, "coverage": 1}]},
#             {"name": "data_right", "value": [{"name": "Locke", "value": 3, "coverage": 0.42}, {"name": "Reyes", "value": 8, "coverage": 0.12}, {"name": "Ford", "value": 45, "coverage": 0.39}]}]
#     return jsonify(data)


if __name__ == '__main__':
    app.run()
