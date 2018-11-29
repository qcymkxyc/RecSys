#! /usr/bin/python3
# coding=utf-8
'''
Created on 2018年6月10日

@author: qcymkxyc
'''
import random


def loadfile(filename):
    """
        根据文件名载入数据
    """
    with open(filename, "r") as f:
        for line in f:
            yield line


def read_rating_data(path="./data/ml-1m/ratings.dat", train_rate=1., seed=1):
    """载入评分数据
        @param path:  文件路径
        @param train_rate:   训练集所占整个数据集的比例，默认为1，表示所有的返回数据都是训练集
        @return: (训练集，测试集) 
    """
    trainset = list()
    testset = list()

    random.seed(seed)
    for line in loadfile(filename=path):
        user, movie, rating, _ = line.split('::')
        if random.random() < train_rate:
            trainset.append([int(user), int(movie), int(rating)])
        else:
            testset.append([int(user), int(movie), int(rating)])
    return trainset, testset


def all_items(path="./data/ml-1m/ratings.dat"):
    """返回所有的movie"""
    items = set()
    for line in loadfile(filename=path):
        _, movie, _, _ = line.split("::")
        items.add(movie)
    return items
