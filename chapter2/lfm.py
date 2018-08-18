#! /usr/bin/python3
# coding=utf8

import sys
sys.path.append("../")
import random
from util import movielen_reader
from operator import itemgetter
from collections import defaultdict

class LFM(object):
    """隐语义模型"""
    def __init__(self,F,learning_rate = 0.01,regularization_rate = 0.1):
        """
            @param F:    隐语义的个数
            @param learning_rate: 梯度下降的学习率
            @param regularization_rate:   正则化率   
        """
        self.F = F
        self.regularization_rate = regularization_rate
        self.learning_rate = learning_rate
        
    def predict(self,user,item):
        """预测用户对商品的喜爱程度
            @param user:
            @param item:  
        """    
        user_F = self.user_matrix[user]
        item_F = self.item_matrix[item]
        
        assert len(user_F) == len(item_F)
        pred = 0.
        for i,score in enumerate(user_F):
            pred += score * item_F[i]
        return pred
    
    def train(self,origin_data,n_epoch,ratio = 1,save_path = "store/lfm.pkl"):
        """
            @param origin_data:    训练集
            @param ratio:    正负样本的比率
            @param n_epoch:    epoch次数
            @param save_path:   保存路径 
        """
        self._init_train(origin_data)   #初始化训练集
        for epoch in range(n_epoch):
            print("正在训练第{}轮".format(epoch))
            for user,items in self.train.items():
                user_samples = self.nagetive_select(items,ratio)  #负采样
                for item in items:
                    eui  = user_samples[item] - self.predict(user, item)
                    for i in range(self.F):
                        p_uk = self.user_matrix[user][i]
                        q_ik = self.item_matrix[item][i]
                        
                        self.user_matrix[user][i] += self.learning_rate * (q_ik * eui - self.regularization_rate * p_uk)
                        self.item_matrix[item][i] += self.learning_rate * (p_uk * eui - self.regularization_rate * q_ik) 
                

    def _init_train(self,origin_data):
        """初始化训练集
            包括
            1. 初始化训练集
            2. 建立商品池
            3. 建立用户以及商品的隐语义矩阵
        """
        self.train = dict()
        self.item_pool = set()  #商品池
        
        self.user_matrix = dict()   #用户的隐语义矩阵
        self.item_matrix = dict()   #商品的隐语义矩阵
        
        for user,item,_ in origin_data:
            self.item_pool.add(item)
            self.train.setdefault(user,set())
            self.train[user].add(item)    
            
            self.user_matrix.setdefault(user,[random.random() for _ in range(self.F)] )
            self.item_matrix.setdefault(item,[random.random() for _ in range(self.F)] )
            
            
    def nagetive_select(self,items,ratio):
        """负样本采样
            @param items:    正样本
            @param ratio:    负样本和正样本的比率
            @return: 包含正样本以及负样本的dict,dict的值1表示正样本0表示负样本
        """
        samples = {item : 1 for item in items}
        nagetive_count = 0;
        while(nagetive_count >= len(items)) * ratio:
            item = random.choice(self.item_pool)
            if item in items:
                continue
            samples[item] = 0
            nagetive_count += 1
        
        return samples
    
    def recommend(self,user,N):
        """
            @param user:
            @param N:    推荐的商品个数
            @return: 商品字典 {商品 : 隐语义打分情况}
        """
        recommends = defaultdict(int)
        related_items = self.train.get(user,list())
        for item in self.item_pool:
            if item in related_items:
                continue
            recommends[item] += self.predict(user, item)
            
        return dict(sorted(recommends.items(),key = itemgetter(1),reverse = True)[:N])
 
    def recommend_users(self,users,N):
        """推荐测试集
            @param users:    用户list
            @param N:    推荐的商品个数
            @return: 推荐字典 {用户 : 推荐的商品的list}
        """
        recommends = dict()
        for user in users:
            user_recommends= list(self.recommend(user, N).keys())
            recommends[user] = user_recommends
            
        return recommends             
        
      

    

    
        
