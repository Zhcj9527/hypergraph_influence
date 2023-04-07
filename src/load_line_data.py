def read_data():
    points = []      #保存数据中的点
    f = open('static\data.txt')   #打开数据文件
    for line in f.readlines():
        p = line.strip().split(' ') #strip 删除空白字符，split是切割返回一个列表
        points.append({'x': int(p[0]), 'y': int(p[1])})   # 按json格式储存
    return points

if __name__ == '__main__':
    data = read_data()