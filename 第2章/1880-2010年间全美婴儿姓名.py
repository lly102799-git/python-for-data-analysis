# -*- coding: utf-8 -*-
"""
@project: python-cookbook
@date: 2021-02-07 9:42
@author: Li Luyao
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_dir = r'F:\Coding\Python for Data Analysis\pydata-book-1st-edition\ch02\names'
names1880 = pd.read_csv(file_dir + r'\yob1880.txt', names=['name', 'sex', 'births'])

# 按性别统计婴儿出生数
print(names1880.groupby('sex')['births'].sum())

# 拼接所有年数据: pandas.concat
# 2010年是数据的最后一个统计年度
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = file_dir + r'\yob{}.txt'.format(str(year))
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year
    pieces.append(frame)

# 将所有数据整合到单个DataFrame中
names = pd.concat(pieces, ignore_index=True)

# 利用groupby或pivot_table在year或sex级别上对names进行聚合操作
total_births = names.pivot_table(values='births', index='year', columns='sex', aggfunc='sum')
total_births.plot(title='Total births by sex and year')

# 按年份和性别对名称占比进行统计
def add_prop(group):
    # births = group['births'].astype(float) # python3 不需要转换成浮点数再除
    births = group['births']

    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)
# prop有效性检查：np.allclose
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

# 为了实现进一步的分析，去除该数据的子集：每对sex/year组合的前1000个名字
# 方式一：
def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)

# 方式二：
pieces = []
for year, group in names.groupby(['year', 'sex']): # 还能这样
    pieces.append(group.sort_values(by='births', ascending=False)[:1000])
top1000 = pd.concat(pieces, ignore_index=True)

# 将index中的year和sex去掉
top1000.index = top1000.index.droplevel() # 按顺序去掉year level
top1000.index = top1000.index.droplevel() # 按顺序去掉sex level

# 将前1000个名字分为男女两个部分
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

# 生成按year和name统计的总出生数透视表
total_births = top1000.pivot_table(values='births', index='year', columns='name', aggfunc='sum')

# 用DataFrame的plot方法绘制几个名字的曲线图
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True, figsize=(12, 10), grid=False, title='Number of births per year')

# 评估命名多样性的增长
table = top1000.pivot_table(values='prop', index='year', columns='sex', aggfunc='sum')
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))

# 2010年男孩的名字
df = boys[boys.year == 2010]
# 计算占出生人数前50%的不同名字的数量
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
# 寻找50%位置：searchsorted()
prop_cumsum.searchsorted(0.5) + 1

# 对比1900年数据：
df = boys[boys.year == 1900]
in1900 = df.sort_values(by='prop', ascending=False).prop.cumsum()
in1900.searchsorted(0.5) + 1

# 现在就可以对所有year/sex组合执行计算
def get_quantile_count(group, q=0.5):
    tmp = group.sort_values(by='prop', ascending=False).prop.cumsum()
    return tmp.searchsorted(q) + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
diversity.plot(title='Number of popular names in top 50%')
