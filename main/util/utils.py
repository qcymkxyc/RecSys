#! /usr/bin/python3
# coding=utf-8
"""
Created on 2018年6月13日

@author: qcymkxyc
"""
import os
import pickle


def save_file(filepath, data):
    """
        保存数据
        @param filepath:    保存路径
        @param data:    要保存的数据
    """
    parent_path = filepath[: filepath.rfind("/")]

    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
    with open(filepath, "wb") as f:
        pickle.dump(data, f)


def load_file(filepath):
    """载入二进制数据"""
    with open(filepath, "rb") as f:
        data = pickle.load(f)
    return data


def open_text(filename,skip_row = 0):
    """打开文本文件

    :param filename: str
        文件名
    :param skip_row: int
         需要跳过的行数
    :return generator
        生成每一行的文本
    """
    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < skip_row:
                continue
            yield line
