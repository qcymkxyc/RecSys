#! /usr/bin/python3
#coding=utf-8
'''
Created on 2018年6月4日

@author: qcymkxyc
'''
from chapter4.basic_tag_rec import TAGRec
import math
from util.delicious_reader import split_data
from collections import defaultdict
from util import metric

class TagBasedTFIDF(TAGRec):
    """TagBasedTFIDF算法
    """
    def init_states(self, data):
        TAGRec.init_states(self, data)
        
        #记录
        self.tag_user= dict()
        for sub_data in data:
            user_id = sub_data[0]
            tag_id = sub_data[-1]
            self.tag_user.setdefault(tag_id,set)
            self.tag_user[tag_id].add(user_id)
            
            
    def recommend(self,user_id):
        """推荐
            @param user_id:
            @return: 推荐的dict ( item_id : 分数) 
        """
        buyed_items = self.user_items[user_id]
        
        recommends = defaultdict(float)
        for tag,tag_time in self.user_tag[user_id].items():
            for item,item_time in self.tag_items[tag].items():
                if item in buyed_items:
                    continue
                recommends[item] += (tag_time / math.log(1 + len(self.tag_user[tag]))) * item_time
        return recommends 
    
    
if __name__ == "__main__":
    filename = "/home/qcymkxyc/mystyle/git/RecSys/data/delicious-2k/user_taggedbookmarks.dat"
    tag_rec = TAGRec()
    train_set,test_data = split_data(filename);
    
    
    tag_rec.init_states(train_set)
     
    test_dict = defaultdict(list)
    for user_id,bookmark_id,tag_id in test_data:
        test_dict[user_id].append(bookmark_id)
    
    recommends = dict()
    for user_id in list(test_dict.keys()):
        recommends[user_id] = tag_rec.recommend(user_id).keys()
    
     
    print("Precision : {}".format(metric.precision(recommends, test_dict)))
    print("Recall : {}".format(metric.recall(recommends, test_dict)))
    
    