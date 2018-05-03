#/usr/bin/python3
#coding=utf8

import random
from collections import defaultdict
import math
from operator import itemgetter
import pickle
import os

class UserCF(object):
    """基于用户的协同过滤"""
    def __init__(self):
        self.trainset = dict()
        self.testset = dict()
        
        #用户相似性矩阵
        self.user_sim_mat = None
        
    
    @staticmethod
    def loadfile(self,path = "./data/ml-1m/ratings.dat"):
        """载入文件"""
        with open(path,"r") as f:
            for i,line in enumerate(f):
                yield line
    
    def read_data(self,path = "./data/ml-1m/ratings.dat",pivot=0.8):
        """读取数据，并返回trainset和testset"""
        for line in UserCF.loadfile(path):
            user, movie, rating, _ = line.split('::')
            if random.random() < pivot :
                self.trainset.setdefault(user,{})
                self.trainset[user][movie] = int(rating)
            else:
                self.testset.setdefault(user,{})
                self.testset[user][movie] = int(rating)
                
    def user_sim(self,save = True):
        """计算用户的相似程度矩阵,save表示是否保存相似矩阵"""
        print("正在载入相似性矩阵....")
        try:
            self.user_sim_mat = self._load_user_sim()
            print("载入相似性矩阵成功")
            return self.user_sim_mat
        except FileNotFoundError:
            print("未找到形式性矩阵，正在准备重新计算..")
            
        print("正在计算用户相似性矩阵")
        print("正在计算电影倒排矩阵.......")
        #建立电影的倒排矩阵
        movie_user_mat = dict()
        for user,movies in self.trainset.items():
            for movie,rating in movies.items():
                movie_user_mat.setdefault(movie,set());
                movie_user_mat[movie].add(user)
        print("倒排矩阵计算完成")
        
        print("开始统计用户共同爱好电影个数.....")
        #用户共同爱好电影个数统计
        user_sim_mat = dict()
        for movie,users in movie_user_mat.items():
            for u in users:
                for v in users:
                    if u == v :
                        continue
                    user_sim_mat.setdefault(u,defaultdict(int))
                    user_sim_mat[u][v] += 1
        print("用户电影个数统计完成")
                    
        print("计算用户相似度矩阵....")
        #建立用户相似度矩阵
        W = dict()
        for u,u_rel in user_sim_mat.items():
            for v,rel_count in u_rel.items():
                W.setdefault(u,{});
                
                u_movies = len(self.trainset[u])
                v_movies = len(self.trainset[v])
                W[u][v] = rel_count / math.sqrt(u_movies * v_movies)
            
        print("相似度矩阵计算完成")
                
        self.user_sim_mat = W
        print("正在保存相似性矩阵...")
        if save : self._save_user_sim()
        print("保存完成")

        return W
    
    def recommend(self,user,N,K):
        """向用户user推荐N个商品，K表示查找和user相似的K个用户"""
        rank = dict()
        for u,u_sim in sorted(self.user_sim_mat.get(user,{}).items(),\
                              key = itemgetter(1),reverse = True)[:K]:
            for movie,rating in self.trainset[u].items():
                rank.setdefault(movie,0.);
                rank[movie] += rating * u_sim
        
        return dict(sorted(rank.items(),key = itemgetter(1),reverse = True)[:N])
    
    def evalute(self,N = 10,K = 80):
        """"""
        print("Presion : {}".format(self.presion(N, K)))
        print("Recall : {}".format(self.recall(N, K)))
        print("训练集 Coverage : {}".format(self.coverage(self.trainset, N, K)))
        print("测试集Coverage : {}".format(self.coverage(self.testset, N, K)))
    
    def presion(self,N = 10,K = 80):
        """"""
        hit = 0.
        all_p = 0.
        
        for user,movies in self.testset.items():
            rank = self.recommend(user, N, K)
            for movie,rating in movies.items():
                if movie in rank.keys():
                    hit += 1.
                all_p += len(movies)
        return hit / all_p
    
    def coverage(self,dataset,N = 10,K = 80):
        recom_item = set()
        all_item = set()
        for user,movies in dataset.items(): 
            for movie,rating in movies.items():
                all_item.add(movie)
                
            rank = self.recommend(user, N, K);
            for movie in rank.keys():
                recom_item.add(movie)
        
        return len(recom_item) / len(all_item)
    
    def recall(self,N = 10,K = 80):
        hit = 0.
        all_r = 0.
        
        for user,movies in self.testset.items():
            rank = self.recommend(user, N, K)
            for movie,rating in movies.items():
                if movie in rank.keys():
                    hit += 1.
                all_r += len(rank)
        return hit / all_r
        
        
    def _save_user_sim(self,path = "store/user_sim.pkl"):
        """存储用户相似性矩阵"""
        dictory = path[:path.rfind("/")]
        if not os.path.exists(dictory):
            os.mkdir(dictory)
        with open(path,"wb") as f:
            pickle.dump(self.user_sim_mat,f)
    
    def _load_user_sim(self,path = "store/user_sim.pkl"):
        with open(path,"rb") as f:
            self.user_sim_mat = pickle.load(f)
        return self.user_sim_mat
        
if __name__ == "__main__":
    usercf = UserCF()
    usercf.read_data(pivot = 0.05)
    usercf.user_sim()
    usercf.evalute()
    