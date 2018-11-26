import unittest
from main.chapter4 import sim_tag_rec
from main.util import delicious_reader
import copy


class SimTagTestCase(unittest.TestCase):
    def setUp(self):
        self.data = delicious_reader.\
            read_tag("../data/delicious-2k/user_taggedbookmarks-timestamps.dat", 1)

    def test_build_tag_vec(self):
        """测试标签向量的建立"""
        model = sim_tag_rec.SimTagTFIDF()
        model._build_tag_vec(self.data)

        self.assertTrue(isinstance(model.tag_vecs, dict))
        self.assertTrue(len(model.tag_vecs) > 0)

    def test_tag_similarity(self):
        """测试两个标签向量的相似性"""
        model = sim_tag_rec.SimTagTFIDF()
        model._build_tag_vec(self.data)

        sim = sim_tag_rec.SimTagTFIDF.tag_similarity(model.tag_vecs[0], model.tag_vecs[5])
        self.assertTrue(isinstance(sim, float))

        tag1_vec = copy.copy(model.tag_vecs[8])
        tag2_vec = copy.copy(model.tag_vecs[8])
        sim = sim_tag_rec.SimTagTFIDF.tag_similarity(tag1=tag1_vec, tag2=tag2_vec)
        self.assertEqual(1, sim)

    def test_tag_vec_report(self):
        sub_data = [i for i in self.data]

        model = sim_tag_rec.SimTagTFIDF()

        with self.assertRaises(AttributeError):
            model.tag_vec_report()
        model._build_tag_vec(sub_data[:10])
        print("Tag Vec:")
        for tag, items in model.tag_vecs.items():
            print("{tag}:{item}".format(tag=tag, item=items))
        print("Tag Vec Report")
        print(model.tag_vec_report(tops=5))

    def test_recommend_user(self):
        """测试推荐"""
        sub_data = [i for i in self.data]
        model = sim_tag_rec.SimTagTFIDF()

        # 不需要标签推荐的情况
        model.train(sub_data[:1000])
        print("user:{}".format(sub_data[101][0]))
        model.recommend(sub_data[101][0], 10)

        # 需要标签推荐的情况
        model.recommend(242, 10)
        self.assertTrue(len(model.user_tag[242]) > model.recommend_least_tag)


if __name__ == '__main__':
    unittest.main()
