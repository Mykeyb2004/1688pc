#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl_pages()
    print("Job is done.")
