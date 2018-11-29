#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 下午2:29
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : tc_itemcf.py
@Software: PyCharm

基于ItemCF的时间上下文推荐

"""
from collections import defaultdict
import math


class TCItemCF:
    """基于时间上下文的ItemCF推荐"""

    def __init__(self):
        self.sim_matrix = None  # 保存相似性矩阵

    def train(self, data):
        """训练

        :param data: list(list(int,int,datetime))
            训练数据（list(list(userID,ItemID,发生时间))）
        """
        self.sim_matrix = TCItemCF.get_similarity(data)  # 计算相似性矩阵

    @staticmethod
    def get_similarity(data, alpha):
        """计算相似性矩阵

        :param data: list(list(int,int,datetime))
            训练数据（list(list(userID,ItemID,发生时间))）
        :param alpha: float
            时间衰减的比率
        :return: dict()
            相似性矩阵
        """
        sim_matrix = defaultdict(lambda: dict())
        item_users = dict()     # 商品对应的购买用户

        # 计算分子部分
        for i, (user1, item1, ui_time1) in enumerate(data):
            item_users.setdefault(item1, 0)
            item_users[item1] += 1
            for j, (user2, item2, ui_time2) in enumerate(data):
                if i == j:
                    continue
                if user1 == user2:
                    sim_matrix[item1].setdefault(item2, 0.)
                    abs_time = abs(ui_time2 - ui_time1).seconds / (60 * 60)  # 以小时为单位
                    sim_matrix[item1][item2] += 1. / (1 + alpha * abs_time)

        # 加入分母
        for item1, items in sim_matrix.items():
            for item2, v in items.items():
                sim_matrix[item1][item2] = v / math.sqrt(item_users[item1] * item_users[item2])

        return sim_matrix
