# -*- coding: utf-8 -*-
"""
@project: python-cookbook
@date: 2021-02-04 10:04
@author: Li Luyao
"""

import pandas as pd

dir_path = r"F:\Coding\Python for Data Analysis\pydata-book-1st-edition\ch02\movielens"

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(dir_path + r"\users.dat", sep='::', header=None, names = unames, engine='python')

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(dir_path + r'\ratings.dat', sep='::', header=None, names=rnames, engine='python')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(dir_path + r'\movies.dat', sep='::', header=None, names=mnames, engine='python')

# 分析散布在三个表中的数据，首先需要将三个表合并
data = pd.merge(pd.merge(ratings, users), movies)

# 现在，就能轻松地根据任意个用户或电影属性对评分数据进行聚合操作了
# 按性别计算每部电影的得分
mean_ratings = data.pivot_table(values='rating', index='title', columns='gender', aggfunc='mean')
# mean_ratings = data.pivot_table(values=['rating'], index=['title'], columns=['gender'], aggfunc=['mean'])

# 过滤掉评分数据不够250条的电影
ratings_by_title = data.groupby('title').size() # Series
active_titles = ratings_by_title.index[ratings_by_title > 250] # Index: 返回ratings_by_title中值大于250的label索引
mean_ratings = mean_ratings.loc[active_titles] # label-based indexing，而不是iloc

# 针对女性最爱看的电影进行排序
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
# top_female_ratings = mean_ratings.sort_values(by=('mean', 'rating', 'F'), ascending=False)

print(top_female_ratings[:10])

# 找出男女评分差异最大的电影
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
# 按diff排序即可得到分歧最大且女性观众更喜欢的电影
sorted_by_diff = mean_ratings.sort_values(by='diff')
print(sorted_by_diff[:15]) # 女性最喜欢
print(sorted_by_diff[::-1][:15]) # 男性最喜欢

# 找出分歧最大的电影，则可以计算得分数据的方差或标准差
rating_std_by_title = data.groupby('title')['rating'].std()
# 根据active_titles进行过滤
rating_std_by_title= rating_std_by_title.loc[active_titles]
# 根据标准差进行降序排序
print(rating_std_by_title.sort_values(ascending=False)[:10])