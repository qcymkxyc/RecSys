# coding=utf8

from main.chapter2 import UserCF
import sys
import random
import numpy as np

filepath = "store/LFM"


class LFM(UserCF):
    """隐语义模型"""
    def __init__(self, k, learning_rate=0.01, regularization_rate=0.1):
        """
            @param k:要分成的类别
            @param learning_rate: 梯度下降的学习率
            @param regularization_rate:   正则化率   
        """
        self.k = k
        self.regularization_rate = regularization_rate
        self.learning_rate = learning_rate
        super().__init__()
        
        # 读取数据
        self.read_data(pivot=0.05)
        # 获取商品集合
        self.item_pool = self.__get_items(self.trainset)
        # 建立隐语义矩阵
        self.__build_matrix()
        
    def __get_items(self, trainset):
        """返回所有商品集"""
        print("开始计算商品集.....",file = sys.stderr)
        items_pool = set()
        for user,items in trainset.items():
            for item in items.keys():
                items_pool.add(item)
        print("商品集计算完成",file = sys.stderr)
        return list(items_pool)
    
    def __build_matrix(self):
        """建立隐语义矩阵"""
        print("开始建立隐语义矩阵....",file = sys.stderr)
        n_users,n_movies = len(self.trainset),len(self.item_pool)
        # 建立用户的隐语义
        self.user_p = dict()
        for user in self.trainset.keys():
            self.user_p[user] = np.random.normal(size = (self.k))
         
        self.movie_q = dict()
        for movie in self.item_pool:
            self.movie_q[movie] = np.random.normal(size = (self.k))
        print("隐语义矩阵建立完成",file = sys.stderr)
            
    def _model_fn(self,n_users,n_movies):
        """主体函数"""
        user_p = np.random.normal(size = (n_users,))

    def select_negatives(self,user_movies):
        """
            采集负样本,使负样本数量和正样本相同
            @param user_movies: 用户对应的正样本
            @return: 正负样本 
        """
        items = dict()
        # 采集正样本
        for movie,rating in user_movies.items():
            items[movie] = rating
        print("开始采集负样本...")
        # 采集负样本
        n_negative = 0;
        while n_negative < len(user_movies):
            negitive_sample = random.choice(self.item_pool)
            if negitive_sample in items:
                continue
            items[negitive_sample] = 0
            n_negative += 1
        
        return items
      
    def loss(self):
        C = 0.
        for user,user_latent in self.user_p.items():
            for movie,movie_latent in self.movie_q.items():
                try:
                    rui = self.trainset[user][movie]
                except KeyError:
                    rui = 0
                eui = rui - self.predict(user,movie)
                C += (np.square(eui) + 
                      self.regularization_rate * np.sum(np.square(self.user_p[user])) +
                      self.regularization_rate * np.sum(np.square(self.movie_q[movie]))
                      ) 
        return C
        
    def predict(self, user, item):
        return np.dot(self.user_p[user],self.movie_q[item])
        
    def train(self, epoches):
        for epoch in range(epoches):
            print("开始第{}轮训练".format(epoch))
            for user,user_movies in self.trainset.items():
                select_samples = self.select_negatives(user_movies)
                for movie,rui in select_samples.items():
                    eui = rui - self.predict(user,movie)
                    user_latent = self.user_p[user]
                    movie_latent = self.movie_q[movie]
                    
                    self.user_p[user] += (self.learning_rate * 
                                          (movie_latent - self.regularization_rate * user_latent))
                    self.movie_q[movie] += (self.learning_rate * (
                                            user_latent - self.regularization_rate * movie_latent))
            print("第{}轮完成".format(epoch))
       
        loss = self.loss()       
        print("loss : {}".format(loss))   

