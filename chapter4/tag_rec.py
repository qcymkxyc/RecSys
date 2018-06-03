# ! /usr/bin/python3 
#coding=utf-8
'''
Created on 2018年6月2日

@author: qcymkxyc
'''
from util.delicious_reader import read_tag
from collections import defaultdict

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
        user_id = str(user_id)
        buyed_items = self.user_items[user_id]
        
        recommends = defaultdict(float)
        for tag,tag_time in self.user_tag[user_id].items():
            for item,item_time in self.tag_items[tag].items():
                if item in buyed_items:
                    continue
                recommends[item] += tag_time * item_time
        return recommends 
            
            
if __name__ == "__main__":
    t = TAGRec()
    s = "/home/qcymkxyc/mystyle/git/RecSys/data/delicious-2k/user_taggedbookmarks.dat"
    data = read_tag(s)
    t.init_states(data)
#     for k,v in t.user_items['57'].items():
#         print(k,v)
    r = t.recommend(57)
    for i,j in r.items():
        print(i,j)

    
