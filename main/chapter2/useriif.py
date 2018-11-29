#!/usr/bin/python3
#coding=utf-8
'''
Created on 2018年6月14日

@author: qcymkxyc
'''

"""
    Ｕser-IIF算法
"""
from main.chapter2 import UserCF
import math
from collections import defaultdict

class UserIIF(UserCF):
    def train(self, origin_data, sim_matrix_path="store/useriif_sim.pkl"):
        UserCF.train(self, origin_data, sim_matrix_path=sim_matrix_path)
        
    def user_similarity(self):
        """建立用户的协同过滤矩阵"""
        #建立用户倒排表
        item_user = dict()
        for user,items in self.train.items():
            for item in items:
                item_user.setdefault(item,set())
                item_user[item].add(user)
                
        #建立用户协同过滤矩阵
        user_sim_matrix = dict()
        N = defaultdict(int)    #记录用户购买商品数
        for item,users in item_user.items():
            for u in users:
                N[u] += 1
                for v in users:
                    if u == v:
                        continue
                    user_sim_matrix.setdefault(u,defaultdict(int))
                    user_sim_matrix[u][v] += 1. / math.log(1 + len(item_user[item]))
        
        #计算相关度
        for u,related_users in user_sim_matrix.items():
            for v,con_items_count in related_users.items():
                user_sim_matrix[u][v] = con_items_count / math.sqrt(N[u] *  N[v])
        
        return user_sim_matrix 