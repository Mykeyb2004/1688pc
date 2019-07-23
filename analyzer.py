#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import dataset
from sqlalchemy import create_engine
from config import *
from utils import *


class Analyzer:
    # pd.set_option('display.max_colwidth', 1000)
    jsonf = 'weight.json'

    def __init__(self):
        self.engine = create_engine(CONNECTION)
        self.df = None
        self.config = load_config(self.jsonf)

    def caculate_weight(self):
        """
         权重计算有两类：
         1. 排名越高权重越大
         2. 排名越趋近某个分位值权重越大
        :return:
        """
        # 从数据库中载入
        print("Loading data from database")
        self.load_data()
        print("sql:\n", self.config['sql'])

        # 初始化权重值
        self.df['weight'] = 0

        # 处理第一类权重算法
        for i, item in enumerate(self.config['top_rank_fields']):
            field = item + '_weight'
            weight = self.get_field_weight(item)
            self.top_rank_weight(item, weight)
            self.df['weight'] = self.df['weight'] + self.df[field]

        # 处理第二类权重算法
        for i, item in enumerate(self.config['percent_rank_fields']):
            field = item + '_weight'
            weight = self.get_field_weight(item)
            self.percent_rank_weight(item, weight)
            self.df['weight'] = self.df['weight'] + self.df[field]

        if DEBUG:
            print("Save data in file [debug.csv].")
            self.df.to_csv("debug.csv")
        self.df.reset_index(level=0, inplace=True)
        # print(self.df[['id', 'price', 'weight']])
        self.update_db()

    def get_field_weight(self, field):
        weights = self.config['weight']
        return weights[field]

    def load_data(self):
        self.df = pd.read_sql(self.config['sql'], self.engine, index_col='id')
        self.df = self.df.replace([None, np.NaN], 0)
        # 计算含物流成本的商品价格
        self.df['price'] = self.df['price1'] + self.df['logistics_cost']

    def top_rank_weight(self, field, weight):
        # 获取权重，排名越高权重越大
        weight_name = field + '_weight'
        # 权重 = 排序位置百分比 * 指标权重
        self.df[weight_name] = self.df[field].rank(numeric_only=None, na_option='bottom', ascending=True,
                                                   pct=True) * weight
        # print(self.df[[field, weight_name]])

    def percent_rank_weight(self, field, weight):
        # 获取权重，排名越靠近指定值，权重越大。指定值为指定的分位值或固定值，计算与该值的差的平方
        rank = field + '_rank'
        # [best_value_rank]的值为0时，则以[best_percent_rank]分位值的数值为最佳值计算权重
        if self.config['best_value_rank'] == 0:
            quantile = self.df[field].quantile(self.config['best_percent_rank'])  # 分位数
        else:  # [best_value_rank]的值为非零值时，则以[best_value_rank]的数值为最佳值计算权重
            quantile = self.config['best_value_rank']
        self.df[rank] = abs(quantile - self.df[field])  # 计算与分位数的距离
        weight_name = field + '_weight'
        # 根据分位数排序情况求百分比位置
        self.df[weight_name] = self.df[rank].rank(numeric_only=None, na_option='bottom', ascending=False,
                                                  pct=True) * weight

    def update_db(self):
        # 将计算的筛选权重保存回数据库中
        db = dataset.connect(CONNECTION)
        table = db[TABLE]
        print("-" * 50)
        # 分别读取id、weight列数据
        pid = self.df['id'].values
        weight = self.df['weight'].values
        # 写入数据库
        for i in range(self.df['id'].count()):
            record = dict(id=pid[i], weight=weight[i])
            table.upsert(record, ['id'])
            print("id = %d\tweight=%f\t%d/%d" % (pid[i], weight[i], (i + 1), self.df['id'].count()))
