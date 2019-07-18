#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from convert_db import Converter

if __name__ == '__main__':
    converter = Converter()
    converter.convert_ads_url()
    print("Job is done.")
