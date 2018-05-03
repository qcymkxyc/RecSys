#/usr/bin/python3
#coding=utf8

import random
from collections import defaultdict

class UserCF(object):
    """基于用户的协同过滤"""
    def __init__(self):
        self.trainset = dict()
        self.testset = dict()
        
    
    @staticmethod
    def loadfile(self,path = "./data/ml-1m/ratings.dat"):
        with open(path,"r") as f:
            for i,line in enumerate(f):
                yield line
    
    @staticmethod
    def read_data(self,path,pivot=0.7):
        """读取数据，并返回trainset和testset"""
        for line in UserCF.loadfile(path):
            user, movie, rating, _ = line.split('::')
            if random.random() < pivot :
                self.trainset.setdefault(user,{})
                self.trainset[user][movie] = int(rating)
            else:
                self.testset.setdefault(user,{})
                self.testset[user][movie] = int(rating)
                
        
if __name__ == "__main__":
    