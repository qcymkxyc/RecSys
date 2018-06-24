#! /usr/bin/python3 
#coding=utf-8
'''
Created on 2018年6月13日

@author: qcymkxyc
'''
import os
import pickle

def save_file(filepath,data):
    """
        保存数据
        @param filepath:    保存路径
        @param data:    要保存的数据
    """
    print(data)
    parent_path = filepath[ : filepath.rfind("/")]
    
    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
    with open(filepath,"wb") as f:
        pickle.dump(data,f)
        
def load_file(filepath):
    """载入数据"""
    with open(filepath,"rb") as f:
        data = pickle.load(f)
    return data
        
        
        

