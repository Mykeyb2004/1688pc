#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from crawler import Crawler
from config import DEBUG

if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl_pages()
    print("Job is done.")
    if DEBUG:
        print("采集程序处于调试模式，仅仅采集部分信息。")
