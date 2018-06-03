# ! /usr/bin/python3 
#coding=utf-8
'''
Created on 2018年6月2日

@author: qcymkxyc
'''
"""
    基本的基于标签的推荐
"""


from util.delicious_reader import split_data
from collections import defaultdict
from util import metric

class TAGRec(object):
    """根据标签推荐"""
    def __init__(self):
        pass
    
    def init_states(self,data):
        """初始化状态"""
        self.user_tag = dict()
        self.tag_items = dict()
        self.user_items = dict()
        
        for user_id,item_id,tag_id in data:
            self.user_tag.setdefault(user_id,defaultdict(int))
            self.user_tag[user_id][tag_id] += 1
            
            self.tag_items.setdefault(tag_id,defaultdict(int))
            self.tag_items[tag_id][item_id] += 1
            
            self.user_items.setdefault(user_id,defaultdict(int))
            self.user_items[user_id][item_id] += 1
            
    
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
                recommends[item] += tag_time * item_time
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
         
    
    

    
