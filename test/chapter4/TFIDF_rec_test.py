#!/usr/bin/python3
# coding=utf-8
"""

@Time    : 18-11-2 下午3:53
@Author  : qcymkxyc
@Email   : qcymkxyc@163.com
@File    : base_rec_test.py
@Software: PyCharm

基本基于标签的推荐测试

"""
import unittest
from main.util import delicious_reader
from main.chapter4 import TagBasedTFIDF


class BaseRecTestCase(unittest.TestCase):

    def test_recommend(self):
        """测试单个用户推荐"""
        data = delicious_reader.read_tag("../data/delicious-2k/user_taggedbookmarks-timestamps.dat", 1)
        base_rec_model = TagBasedTFIDF()

        # 未训练
        with self.assertRaises(AttributeError):
            base_rec_model.recommend(8, 3)

        # 正常推荐
        base_rec_model.train(data)

        user_id = 10523
        self.assertEqual(10, len(base_rec_model.recommend(user_id, 10)))
        self.assertTrue(isinstance(base_rec_model.recommend(user_id, 10), list))
        recommend = base_rec_model.recommend(user_id, 10)
        for i in recommend:
            self.assertFalse(isinstance(i, tuple))

        # 冷启动
        self.assertEqual(10, len(base_rec_model.recommend(-1, 10)))

    def test_recommend_users(self):
        """测试多个用户推荐"""
        users = [8, 32, 10523]

        base_rec_model = TagBasedTFIDF()
        train, test = delicious_reader.split_data("../data/delicious-2k/user_taggedbookmarks-timestamps.dat", k=1)
        base_rec_model.train(train)
        recommends = base_rec_model.recommend_users(users, 10)

        for user, recommend in recommends.items():
            self.assertEqual(10, len(recommend))
            self.assertTrue(user in users)

        transform_test = dict()
        for user_id, item_id, tag_id in test:
            transform_test.setdefault(user_id, [])
            transform_test[user_id].append(item_id)

        temp_test = dict(list(transform_test.items())[:10])
        recommend_user = list(temp_test.keys())
        recommends = base_rec_model.recommend_users(recommend_user, 10)

        for user_id, items in recommends.items():
            print("{user}:{item}".format(user=user_id, item=items))
        for user_id, items in temp_test.items():
            print("{user}:{item}".format(user=user_id, item=items))
