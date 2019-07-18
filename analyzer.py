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
        self.sql = load_config(self.jsonf)['sql']

    def caculate_weight(self):
        """
         权重计算有两类：
         1. 排名越高权重越大
         2. 排名越趋近某个分位值权重越大
        :return:
        """
        # 从数据库中载入
        self.load_data()
        print("sql:\n", self.sql)

        # 初始化权重值
        self.df['weight'] = 0

        # 处理第一类权重算法
        for i, item in enumerate(load_config(self.jsonf)['top_rank_fields']):
            field = item + '_weight'
            weight = self.get_field_weight(item)
            self.top_rank_weight(item, weight)
            self.df['weight'] = self.df['weight'] + self.df[field]

        # 处理第二类权重算法
        for i, item in enumerate(load_config(self.jsonf)['percent_rank_fields']):
            field = item + '_weight'
            weight = self.get_field_weight(item)
            self.percent_rank_weight(item, weight)
            self.df['weight'] = self.df['weight'] + self.df[field]

        if DEBUG:
            print("Save data in file[data.csv].")
            self.df.to_csv("data.csv")
        self.df.reset_index(level=0, inplace=True)
        # print(self.df[['id', 'weight']])
        self.update_db()

    def get_field_weight(self, field):
        weights = load_config(self.jsonf)['weight']
        return weights[field]

    def load_data(self):
        self.df = pd.read_sql(self.sql, self.engine, index_col='id')
        self.df = self.df.replace([None, np.NaN], 0)
        # 计算含物流成本的商品价格
        self.df['price'] = self.df['price1'] + self.df['logistics_cost']
        # print(self.df)

    def top_rank_weight(self, field, weight):
        # 获取权重，排名越高权重越大
        weight_name = field + '_weight'
        # 权重 = 排序位置百分比 * 指标权重
        self.df[weight_name] = self.df[field].rank(numeric_only=None, na_option='bottom', ascending=True,
                                                   pct=True) * weight
        # print(self.df[[field, weight_name]])

    def percent_rank_weight(self, field, weight):
        # 获取权重，排名越靠近指定值，权重越大。指定值为指定的分位值，计算与该值的差的平方
        rank = field + '_rank'
        quantile = self.df[field].quantile(load_config(self.jsonf)['best_percent_rank'])  # 分位数
        self.df[rank] = abs(quantile - self.df[field])  # 计算与分位数的距离
        weight_name = field + '_weight'
        # 根据分位数排序情况求百分比位置
        self.df[weight_name] = self.df[rank].rank(numeric_only=None, na_option='bottom', ascending=False,
                                                  pct=True) * weight
        # print(self.df[[field, rank, weight_name]])

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
