#!/usr/bin/python3
# coding=utf-8
'''
Created on 2018年6月15日

@author: qcymkxyc
'''
from main.chapter2 import UserCF
from collections import defaultdict
import math
from operator import itemgetter
import sys
from main.util.utils import load_file, save_file


class ItemCF(UserCF):
    """基于物品的协同过滤矩阵"""

    def __init__(self):
        pass

    def train(self, origin_data, sim_matrix_path="store/item_sim.pkl"):
        """训练模型
            @param origin_data: 原始数据
            @param sim_matrix_path:  协同矩阵保存的路径
        """
        self.origin_data = origin_data
        # 初始化训练集
        UserCF._init_train(self, origin_data)
        print("开始训练模型", file=sys.stderr)
        try:
            print("开始载入用户协同矩阵....", file=sys.stderr)
            self.item_sim_matrix = load_file(sim_matrix_path)
            print("载入协同过滤矩阵完成", file=sys.stderr)
        except BaseException:
            print("载入用户协同过滤矩阵失败，重新计算协同过滤矩阵", file=sys.stderr)
            # 计算用户协同矩阵
            self.item_sim_matrix = self._item_similarity()

        print("开始保存协同过滤矩阵", file=sys.stderr)
        save_file(sim_matrix_path, self.item_sim_matrix)
        print("保存协同过滤矩阵完成", file=sys.stderr)

    def _item_similarity(self):
        """计算商品协同矩阵
            @return: 物品的协同矩阵
        """
        item_sim_matrix = dict()    # 物品的协同矩阵
        N = defaultdict(int)    # 每个物品的流行度

        # 统计同时购买商品的人数
        for _, items in self.train.items():
            for i in items:
                item_sim_matrix.setdefault(i, dict())
                # 统计商品的流行度
                N[i] += 1

                for j in items:
                    if i == j:
                        continue
                    item_sim_matrix[i].setdefault(j, 0)
                    item_sim_matrix[i][j] += 1

        # 计算物品协同矩阵
        for i, related_items in item_sim_matrix.items():
            for j, related_count in related_items.items():
                item_sim_matrix[i][j] = related_count / math.sqrt(N[i] * N[j])

        return item_sim_matrix

    def recommend(self, user, N, K):
        """推荐
            @param user:   用户
            @param N:    推荐的商品个数
            @param K:    查找最相似的商品个数
            @return: 商品字典 {商品 : 相似性打分情况}
        """
        recommends = dict()
        items = self.train[user]
        for item in items:
            for i, sim in sorted(self.item_sim_matrix.get(item, {}).items(), key=itemgetter(1), reverse=True)[: K]:
                if i in items:
                    continue
                recommends.setdefault(i, 0.)
                recommends[i] += sim

        return dict(sorted(recommends.items(), key=itemgetter(1), reverse=True)[: N])

    def recommend_users(self, users, N, K):
        return UserCF.recommend_users(self, users, N, K)
