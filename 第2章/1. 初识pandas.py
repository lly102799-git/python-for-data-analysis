# -*- coding: utf-8 -*-
"""
@project: python-cookbook
@date: 2021-02-03 10:08
@author: Li Luyao
"""
import json

path = r'F:\Coding\Python for Data Analysis\pydata-book-1st-edition\ch02\usagov_bitly_data2012-03-16-1331923249.txt'
# open(path).readline() # 读取一行数据
records = [json.loads(line) for line in open(path)]

# 统计时区
time_zones = [rec['tz'] for rec in records if 'tz' in rec]


def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


# 更简洁的写法
from collections import defaultdict


def get_counts2(sequence):
    counts = defaultdict(int)  # 所有的值均会被初始化为0
    for x in sequence:
        counts[x] += 1
    return counts


counts = get_counts(time_zones)
print(counts['America/New_York'])
print(len(time_zones))


def top_counts(count_dict, n):
    value_key_pairs = [(count, key) for key, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


print(top_counts(counts, n=10))

# 使用python标准库：collections.Counter类
from collections import Counter
counts = Counter(time_zones)
print(counts.most_common(10))

# 用pandas对时区进行计数
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

frame = DataFrame(records)
print(frame['tz'][:10])

# frame['tz']返回的Series对象有一个value_counts方法
tz_counts = frame['tz'].value_counts()
print(tz_counts[:10])

# 使用fillna函数可以替换缺失值（NA），而未知值（如空字符串）则可通过布尔型数组索引加以替换
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown' # Series布尔型数组索引
tz_counts = clean_tz.value_counts() # **kwargs: ascending=True, normalize=True
print(tz_counts[:10])

import matplotlib.pyplot as plt
tz_counts[:10].plot(kind='barh', rot=0)
# plt.barh(tz_counts[:10].index, tz_counts[:10].values) # Series.index和Series.values
# plt.show()

# 解析frame中‘a'(agent)信息
agent_results = Series([x.split()[0] for x in frame.a.dropna()])
print(agent_results[:5])
print(agent_results.value_counts()[:8])

# 根据Windows和非Windows用户对时区统计信息进行分解
cframe = frame[frame.a.notnull()] # 移除确实agent的数据
operating_system = np.where(cframe['a'].str.contains('Windows'),
                            'Windows', 'Not Windows')
print(operating_system[:5])
by_tz_os = cframe.groupby(['tz', operating_system])

agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10])

# 选取最常出现的时区
indexer = agg_counts.sum(1).argsort()
print(indexer[:10])
count_subset = agg_counts.take(indexer)[-10:]
print(count_subset)
# 绘制堆叠条形图
count_subset.plot(kind='barh', stacked=True)

# 相对比例
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)