#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from analyzer import Analyzer

if __name__ == '__main__':
    print("Json文件的权重计算规则说明：")
    print("=" * 30)
    print("""
    【sql】：\t查询语句
    【top_rank_fields】：\t以最大值为最优值的权重计算字段
    【percent_rank_fields】：\t以分位数为最优值的权重计算字段
    【best_percent_rank】：\t指定的最优分位数
    【best_value_rank】：\t指定固定数值为最优值。若为非零值，则忽略【percent_rank_fields】分位数。
    【weight】：\t各字段的加权权重，总和最好为100。
    """)
    print("=" * 30)
    analyzer = Analyzer()
    analyzer.caculate_weight()
    print("Job is done.")
