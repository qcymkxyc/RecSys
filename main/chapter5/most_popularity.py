#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 下午1:04
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : most_popularity.py
@Software: PyCharm

推荐近期最热门的商品

"""
from collections import defaultdict
from operator import itemgetter
import datetime


class RecentPopular:
    """近期最热门的商品"""

    def __init__(self):
        # 物品流行度
        self.item_popularity = defaultdict(lambda: float(0))
        # 保存训练数据
        self.data = None

    def train(self, data):
        """训练

        :param data: list(list(int,int,datetime))
             数据集，（用户ID,ItemID,时间）
        """
        self.data = data

    def recommend(self, alpha, top_n=10, time=datetime.datetime.now()):
        """推荐

        :param alpha: float
            时间的衰减因子
        :param top_n: int
            推荐个数
        :param time: datetime.datetime
            用于计算某个时间的流行度
        :return: list(int)
            商品ID
        """
        for user_id, item_id, ui_time in self.data:
            self.item_popularity[item_id] += 1. / (1 + alpha * (time - ui_time).days)

        recommend_items = sorted(self.item_popularity.items(), key=itemgetter(1), reverse=True)[:top_n]
        return [itemgetter(0)(item) for item in recommend_items]
