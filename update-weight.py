#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from analyzer import Analyzer

if __name__ == '__main__':
    print("Start to load data...")
    analyzer = Analyzer()
    analyzer.caculate_weight()
    print("Job is done.")
