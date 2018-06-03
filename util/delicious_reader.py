#! /usr/bin/python3
#coding=utf-8
'''
Created on 2018年6月2日

@author: qcymkxyc

关于delicious数据集读取集
'''
import random

def read_tag(filename):
    """读取标签数据集
        @param filename:  文件名 
        @return: 三元组(user_id,bookmark_id,tag_id)
    """
    with open(filename) as f:
        for line_data in f:
            user_id,bookmark_id,tag_id = line_data.split("\t")[:3]
            yield (user_id.strip(),bookmark_id.strip(),tag_id.strip())

def split_data(filename,k = 0,cv_folder = 10,seed = 1):
    """用cross validation分离训练集以及测试集
        @param filename: 文件名
        @param k:  cross validation 的第k轮
        @param cv_folder: cross validation的总轮数
        @param seed:  random的seed    
        @return: 训练集，测试集。均以三元组(user_id,bookmark_id,tag_id)形式返回
    """
    train_set = []
    test_set = []
    
    random.seed(seed)
    for sub_data in read_tag(filename):
        if random.randint(0,cv_folder) == k:
            test_set.append(sub_data)
        else:
            train_set.append(sub_data)
            
    return train_set,test_set
    
