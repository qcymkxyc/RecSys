#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 18-11-2 下午2:03
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : base_rec.py
@Software: PyCharm

基本基于标签的推荐

"""
from collections import defaultdict
from operator import itemgetter


# TODO 效果不佳
class BaseRec:
    """基本的基于标签的推荐"""

    def __init__(self):
        # 保存商品的流行度
        self.items_popularity = None
        # 保存训练集
        self.train_data = list()

    def train(self, origin_data):
        """训练模型

        :param origin_data: list
            原始数据，即训练集，list中的元素以(user_id,bookmark_id,tag_id)
            三元组的形式存储
        """
        for user_id, item_id, tag_id in origin_data:
            self.train_data.append((user_id, item_id, tag_id))

        self._build_matrix(self.train_data)

    def _build_matrix(self, train):
        """建立算法对应的字典

        1. 用户-标签字典
        2. 标签-物品字典
        3. 用户已经购买的物品字典

        :param train: list((int,int,int))
            训练集, list中的元素以(user_id,bookmark_id,tag_id)
            三元组的形式存储
        """
        self.user_tag = defaultdict(lambda: {})     # 用户 - 标签字典
        self.tag_item = defaultdict(lambda: {})     # 商品 - 标签字典
        self.user_item = defaultdict(lambda: list())       # 用户已经购买的商品

        for user_id, item_id, tag_id in train:
            self.user_tag[user_id].setdefault(tag_id, 0)
            self.user_tag[user_id][tag_id] += 1

            self.tag_item[tag_id].setdefault(item_id, 0)
            self.tag_item[tag_id][item_id] += 1

            self.user_item[user_id].append(item_id)

    def _code_start(self, rec_count):
        """冷启动

        :param rec_count: int
            推荐个数
        :return: list
            推荐的商品
        """
        if not self.items_popularity:
            self.items_popularity = dict()
            for tag, tag_items in self.tag_item.items():
                for item_id, count in tag_items.items():
                    self.items_popularity.setdefault(item_id, 0)
                    self.items_popularity[item_id] += count

        recommends = sorted(self.items_popularity.items(), key=itemgetter(1), reverse=True)[:rec_count]
        recommends = list(map(itemgetter(0), recommends))

        return recommends

    def _recommend_user(self, user):
        """给用户推荐商品

        :param user: int
            user_id
        :return: dict(int:int)
            排序后的商品推荐的打分情况{item_id:打分情况}（从高到低）
        """
        user_tags = self.user_tag[user]
        recommend_dict = dict()

        user_buys = self.user_item[user]  # 用户已经买过的商品
        for tag_id, tag_count in user_tags.items():
            for item_id, item_count in self.tag_item[tag_id].items():
                # 如果已经买过则不加入推荐名单中
                if item_id in user_buys:
                    continue

                recommend_dict.setdefault(item_id, 0)
                recommend_dict[item_id] += tag_count * item_count

        recommends = sorted(recommend_dict.items(), key=itemgetter(1), reverse=True)
        return recommends

    def recommend(self, user, rec_count):
        """给定用户推荐商品

        如果用户在训练集中未出现(即冷启动问题)，则推荐最热门的商品(对应打标签最多)

        :param user: int
            用户ID
        :param rec_count: int
            推荐数量
        :return: list
            推荐商品ID的list
        :raises:
            AttributeError : 模型未训练
        """
        try:
            user_tags = self.user_tag[user]
        except AttributeError:
            raise AttributeError("模型未训练!")
        else:
            # 冷启动问题
            if len(user_tags) == 0:
                recommends = self._code_start(rec_count)
            # 正常推荐
            else:
                recommends = self._recommend_user(user=user)[:rec_count]
                recommends = list(map(itemgetter(0), recommends))

        return recommends

    def recommend_users(self, users, recommend_count):
        """给多个用户推荐商品

        :param users: list
            用户list
        :param recommend_count: int
            推荐的商品个数
        :return: dict : {用户ID:[推荐商品1，推荐商品2，......]}
            推荐的商品字典
        """
        user_recommends = dict()
        for user in users:
            user_recommends[user] = self.recommend(user, recommend_count)
        return user_recommends
