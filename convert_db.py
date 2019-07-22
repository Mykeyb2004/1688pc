#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dataset
from ads_url import AdsUrl
from utils import get_pc_url
from config import *


class Converter:

    def __init__(self):
        self._db = dataset.connect(CONNECTION)
        self._table = self._db[TABLE]

    def convert_ads_url(self):
        # 查询所有Url字段为空值的数据，将其中的广告链接进行转化，非广告链接则直接填入Url
        sql = "SELECT id, ads_url, url FROM {} WHERE url IS NULL".format(TABLE)
        records = self._db.query(sql)

        if not records:
            print("No record need to be converted.")
            return

        ads = AdsUrl()
        run_times = 0
        # print("There are %d records to be converted." % len(list(tab)))
        for i, row in enumerate(records):
            if row['ads_url'].startswith('https://dj.1688.com'):
                run_times += 1
                print(row['id'], row['ads_url'])

                url = ads.get_url(row['ads_url'])
                url = get_pc_url(url)
                print(url)
                self.update_ads_url(dict(id=row['id'], url=url))
                if DEBUG and run_times >= 2:
                    break
            else:
                print("Saving {}".format(row['ads_url']))
                self.update_ads_url(dict(id=row['id'], url=row['ads_url']))

    def update_ads_url(self, record):
        self._table.update(record, ['id'])
