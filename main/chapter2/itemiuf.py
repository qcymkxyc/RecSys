#!/usr/bin/python3
#coding=utf-8
'''
Created on 2018年6月24日

@author: qcymkxyc
'''
from main.chapter2 import ItemCF
from collections import defaultdict
import math

class ItemIUF(ItemCF):
    """ItemCF-IUF"""
    
    def train(self, origin_data, sim_matrix_path="store/itemiuf_sim.pkl"):
        ItemCF.train(self, origin_data, sim_matrix_path=sim_matrix_path)
        
        
    def _item_similarity(self):
        item_sim_matrix = dict()#物品的协同矩阵
        N = defaultdict(int)#每个物品的流行度
        
        #统计同时购买商品的人数
        for _,items in self.train.items():
            for i in items:
                item_sim_matrix.setdefault(i,dict())
                #统计商品的流行度
                N[i] += 1
                
                for j in items:
                    if i == j:
                        continue
                    item_sim_matrix[i].setdefault(j,0)
                    item_sim_matrix[i][j] += 1. / math.log1p(len(items) * 1.)
        
        #计算物品协同矩阵        
        for i,related_items in item_sim_matrix.items():
            for j,related_count in related_items.items():
                item_sim_matrix[i][j] = related_count / math.sqrt(N[i] * N[j])
            
                        
        return item_sim_matrix
        
