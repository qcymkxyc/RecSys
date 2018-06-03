#! /usr/bin/python3
#coding=utf-8
'''
Created on 2018年6月2日

@author: qcymkxyc

关于delicious数据集读取集
'''

def read_tag(filename):
    """读取标签数据集
        @param filename:  文件名 
        @return: 三元组(user_id,bookmark_id,tag_id)
    """
    with open(filename) as f:
        for line_data in f:
            user_id,bookmark_id,tag_id = line_data.split("\t")[:3]
            yield (user_id,bookmark_id,tag_id)


if __name__ == "__main__":
    s = "/home/qcymkxyc/mystyle/git/RecSys/data/delicious-2k/user_taggedbookmarks.dat"
    a = read_tag(s)
    for i in a:
        print(i)