# RecSys
项亮的《推荐系统实践》的代码实现以及结果展示分析，所有结果见:

>[Recommend System](Recommend%20System.ipynb)

## 第一章
第一章主要介绍一些推荐系统的评价指标

   * [评价指标](util/metric.py)
## 第二章
第二章介绍推荐系统一些基本的模型。这里实验的数据同书上用[MovieLen](data/ml-1m/README)数据集。整个第二章实验包括前半部分的[流行度分析](Recommend%20System.ipynb#%E7%94%A8%E6%88%B7%E8%A1%8C%E4%B8%BA%E5%88%86%E6%9E%90)以及后半部分基于[MovieLen](data/ml-1m/README)的推荐算法(协同过滤第一次运算会生成协同矩阵，会比较慢):

  * [用户协同过滤](chapter2/usercf.py)
  * [商品协同过滤](chapter2/itemcf.py)
  * [UserCF-IIF](chapter2/useriif.py)
  * [ItemCF-IUF](chapter2/itemiuf.py)
  * [ItemCF-Norm](chapter2/itemnorm.py)
  * [隐语义模型](chapter2/lfm.py)

## 第三章
 
第三章主要讲冷启动问题：

   * 用户冷启动
       1. 根据用户信息特征分组推荐
       2. 外站信息导入
       3. 根据用户首次进入反馈的兴趣点
   * 物品冷启动
       1. 基于物品内容信息提取
       2. 人工标注信息

## 第四章

介绍基于标签的推荐。数据集用[Delicious](data/delicious-2k/readme.txt)数据集(对于冷启动问题推荐热门商品)。

   * [基本基于标签推荐](chapter4/base_rec.py)

