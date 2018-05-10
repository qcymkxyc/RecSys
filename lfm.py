#! usr/bin/python3
# coding=utf8

import tensorflow as tf
from usercf import UserCF
import pandas as pd

filepath = "store/LFM"

class LFM(object):
    """隐语义模型"""
    def __init__(self,data,k,learning_rate,regularization_rate):
#         self.model = tf.estimator.Estimator()
        self.k = k
        self.trainset = data
        self.testset = None
        self.regularization_rate = regularization_rate
        self.learning_rate = learning_rate
        
    
    def load_file(self):
        dataset = tf.data.TextLineDataset("./data/ml-1m/ratings.dat")
        print(dataset)
        return dataset
    
    def _model_fn(self,n_users,n_movies):
        """主体函数"""
        p = tf.Variable(
                    initial_value = tf.random_normal(shape = (n_users,self.k)),
                    name = "p")
        q = tf.Variable(
                    initial_value = tf.random_normal(shape = (self.k,n_movies)),
                    name = "q")
        pred_y = tf.matmul(p, q)
        
#         loss = tf.reduce_mean(tf.square(self.trainset - pred_y) + \
#                               self.regularization_rate * p * p + \
#                               self.regularization_rate * q * q)
        loss = tf.reduce_mean(tf.square(self.trainset - pred_y))
        self.loss = loss
        
        optimizer = tf.train.GradientDescentOptimizer(self.learning_rate)
        train_op = optimizer.minimize(loss,global_step = tf.train.get_global_step())
        return train_op
    
    def select_negatives(self,data):
        """采集负样本"""
        
        
    def train(self):
        train_op = self._model_fn(1, 1);
        with tf.Session() as session:
            session.run(tf.initialize_all_variables())
            for i in range(1000):
                session.run(train_op)
                if i % 100 == 0:
                    print(session.run(self.loss))
    
def read_data():
    data = dict()
    for i,line in enumerate(UserCF.loadfile()):
        user, movie, rating, _ = line.split('::')
        data.setdefault(movie,{})
        data[movie][user] = rating
    df = pd.DataFrame(data)
    df.to_csv("a.csv",index = True)
                        
if __name__ == "__main__":
#     read_data()
    data = pd.read_csv("a.csv")
    data.fillna(0,inplace = True)
    
    lfm = LFM(
        data = data.values,
        k = 5,
        learning_rate = 0.1,
        regularization_rate = 0.1)
    
    lfm.train()
#     lfm.load_file()
    

    
        