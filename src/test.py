# -*- coding: utf-8 -*-
"""
@Time ： 2022/7/6 13:08
@Auth ： zhcj
@File ：test.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

result = [[3, 4], [3, 4], [2, 3, 4], [2, 3, 4], [0, 2, 3, 4], [0, 2, 3, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4],
          [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4],
          [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4], [0, 2, 4]]

# control the length of sequence

num = 5
list_5 = []
length = len(result)
count = 0
t = 0

while length>=5:
    for i in range(length):
        count += 1
        if count == num:
            for itm in range(num):
                list_5.append(result[itm])
            print(list_5)
            result.pop(0)  ## 删除第一个元素
            length = len(result)
            count = 0
            list_5 = []  ## 清空列表