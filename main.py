#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from crawler import Crawler
from combine import Combiner

if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl_pages()
    # combine_data = Combiner()
    # print(combine_data.product_name)
    # combine_data.product_name = ['test', 'sf']
    # print(combine_data.product_name)
