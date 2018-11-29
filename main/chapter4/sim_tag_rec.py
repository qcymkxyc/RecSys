#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 下午1:14
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : sim_tag_rec.py
@Software: PyCharm

考虑数据的稀疏性，添加标签的相似度

"""
from main.chapter4 import TagBasedTFIDFPlus
from collections import defaultdict
from operator import itemgetter
import math
import pandas as pd


class SimTagTFIDF(TagBasedTFIDFPlus):
    """
    在TagBasedTFIDFPlus的基础上添加标签相似性的衡量，
    以应对数据稀疏性问题
    """
    recommend_least_tag = 20    # 推荐相关标签的限额

    def __init__(self):
        TagBasedTFIDFPlus.__init__(self)
        self.tag_vecs = None     # 标签向量

    def train(self, origin_data):
        TagBasedTFIDFPlus.train(self, origin_data)
        # 构建标签向量
        self._build_tag_vec(self.train_data)

    def _build_tag_vec(self, train):
        """构建标签向量

        tag_vec(标签向量)为一个dict{int,{}},外层的key表示标签的id,内层的dict的key
        为item的id，value为给item打标签的用户数(即打标签的次数)

        :param train: tuple(int,int,int)
            训练集(用户ID,item_id,tag_id)
        """
        self.tag_vecs = defaultdict(lambda: {})
        for user_id, item_id, tag_id in train:
            self.tag_vecs[tag_id].setdefault(item_id, 0)
            self.tag_vecs[tag_id][item_id] += 1

    @staticmethod
    def tag_similarity(tag1, tag2):
        """计算两个标签的相似度

        :param tag1: dict {int, int)
            标签1，dict(item_id: 被标记的个数)
        :param tag2: dict {int, int}\
            标签2，格式同标签1
        :return: float
            相似度
        """
        similarity = 0.
        tag1_norm, tag2_norm = 0., 0.  # tag1和tag2的范数

        for item_id, count in tag1.items():
            tag1_norm += count**2
            similarity += count * tag2.get(item_id, 0.)

        for item_id, count in tag2.items():
            tag2_norm += count**2

        try:
            similarity = similarity / math.sqrt(tag1_norm * tag2_norm)
        # 防止标签为空的情况
        except ZeroDivisionError:
            similarity = 0.
        finally:
            return similarity

    def tag_vec_report(self, tops=10):
        """打印标签相似度的报告

        :param tops: int
            取热度最大的前多少个
        :return: pd.DataFrame
            相似性矩阵
        :raises:
            AttributeError : 模型未训练
        """
        if not self.tag_vecs:
            raise AttributeError("模型未训练")

        similarity_matrix = defaultdict(lambda: list())    # 标签的相似性矩阵
        tag_vec_item = sorted(self.tag_vecs.items(), key=lambda x: sum(x[1].values()), reverse=True)[:tops]

        for i, (tag1_id, tag1_items) in enumerate(tag_vec_item):
            for j, (tag2_id, tag2_items) in enumerate(tag_vec_item):
                # 矩阵对角线上的为1
                if i == j:
                    similarity_matrix[tag1_id].append(1.)
                # 对角已经计算过
                elif i > j:
                    similarity_matrix[tag1_id].append(similarity_matrix[tag2_id][i])
                # 未计算过
                else:
                    similarity_matrix[tag1_id].append(
                        SimTagTFIDF.tag_similarity(tag1_items, tag2_items))

        return pd.DataFrame(similarity_matrix, index=similarity_matrix.keys())

    def _recommend_user(self, user):
        """给用户推荐商品

        如果用户的本身拥有的标签过少，则用协同过滤推荐相关标签
        再利用相关的标签的信息推荐物品

        :param user: int
            user_id
        :return: dict(int:int)
            排序后的商品推荐的打分情况{item_id:打分情况}（从高到低）
        """
        user_tags = self.user_tag[user]
        # 如果用户标记的标签过少则推荐相关的标签
        if len(user_tags) < SimTagTFIDF.recommend_least_tag:
            recommends = dict()
            for tag_id, tag_vec in self.tag_vecs.items():   # 所有标签循环
                for user_tag, _ in user_tags.items():      # 当前用户所用的标签循环
                    # 跳过用户已使用的标签
                    if tag_id in user_tags.keys():
                        continue
                    user_tag_vec = self.tag_vecs[user_tag]      # 当前用户的标签向量
                    recommends[tag_id] = self.tag_similarity(tag_vec, user_tag_vec)
            recommends = sorted(recommends.items(), key=itemgetter(1),reverse=True)[:SimTagTFIDF.recommend_least_tag]
            recommends = dict(recommends)
            self.user_tag[user] = {**user_tags, **recommends}

        # 综合相关标签信息推荐
        return TagBasedTFIDFPlus._recommend_user(self, user)
