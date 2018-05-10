#/usr/bin/python3 
#coding=utf8

from usercf import UserCF
from collections import defaultdict
import math
import os
import sys
import pickle
from operator import itemgetter

class ItemCF(UserCF):
    """基于物品的协同过滤"""

    def item_sim(self,save = True):
        """商品的相似性矩阵"""
        print("正在载入相似性矩阵....")
        try:
            self.item_sim_mat = self._load_item_sim()
            print("载入相似性矩阵成功")
            return self.item_sim_mat
        except FileNotFoundError:
            print("未找到形式性矩阵，正在准备重新计算..")
            
        print("开始计算用户倒排列表....")
        user_movie_mat = dict()
        N = defaultdict(int)
        
        for user,movies in self.trainset.items():
            user_movie_mat.setdefault(user,set())
            for movie in movies.keys():
                N[movie] += 1
                user_movie_mat[user].add(movie)
        print("倒排列表计算完成")
        
         
        print("开始统计物品相关个数......")
        C = dict()
        for user,movies in user_movie_mat.items():
            for i in movies:
                C.setdefault(i,defaultdict(int))
                for j in movies:
                    if i == j :
                        continue
                    C[i][j] += 1
        print("物品个数统计完成")
                     
        print("开始计算物品相似性矩阵....")
        W = dict()
        for i,movies in C.items():
            for j,count in movies.items():
                W.setdefault(i,{})
                W[i][j] = C[i][j] / math.sqrt(N[i] * N[j])
        
        print("物品个数统计完成")
        
        self.item_sim_mat = W
        if save : self._save_item_sim()
        return W
    

    def recommend(self,user,N,K):
        rank = defaultdict(float)
        user_movie = self.trainset[user]
        for movie,rating in user_movie.items():
            for rel_mov,rel_sim in sorted(self.item_sim_mat.get(movie,{}).items(),\
                                          key = itemgetter(1),reverse = True)[:K]:
                rank[rel_mov] += rating * rel_sim
                
        return dict(sorted(rank.items(),key = itemgetter(1),reverse = True)[:N])
    
    def _save_item_sim(self,path = "store/item_sim.pkl"):
        """存储物品相似性矩阵"""
        dictory = path[:path.rfind("/")]
        if not os.path.exists(dictory):
            os.mkdir(dictory)
        with open(path,"wb") as f:
            pickle.dump(self.item_sim_mat,f)
    
    def _load_item_sim(self,path = "store/item_sim.pkl"):
        with open(path,"rb") as f:
            self.item_sim_mat = pickle.load(f)
        return self.item_sim_mat
    
if __name__ == "__main__":
    itemcf = ItemCF();
    itemcf.read_data(pivot = 0.8)
    itemcf.item_sim()
    itemcf.evalute(N = 10,K = 20)
#     print(itemcf._load_item_sim())