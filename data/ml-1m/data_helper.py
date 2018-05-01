# /usr/bin/Python2
#coding=utf8

def loadfile(path):
    with open(path,"r") as f:
        for i,line in enumerate(f):
            yield line

def read_users(path = "users.dat"):
    """
                返回user的list
        Args:
            path :    文件路径
        Return:
            user的list形式,格式为（userId,性别，年龄，职业）
    """
    users = []
    for line in loadfile(path):
        users.append(line.split("::")[:-1])
    return users

def read_movies(path = "movies.dat"):
    """
                返回movie的list
        Args:
            path :    文件路径
        Return:
            movie的list形式,格式为（movieId,电影名，类型）
    """
    movies = []
    for line in loadfile(path):
        movies.append(line.split("::"))
    return movies

def read_ratings(path):
    """
        Return:
            rating的list形式，形式为（UserId，movieID，Rating，tempstamp）
    """
    ratings = dict()
    for line in loadfile(path):
        user,movie,rating,_ = line.split("::")
        ratings.setdefault(user,{});
        ratings[user][movie] = int(rating)
    
    return ratings

