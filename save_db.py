#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dataset


class Saver:

    def __init__(self):
        self._db = dataset.connect('mysql://root:mini08!@192.168.0.220:3306/1688?charset=utf8')
        self._table = self._db['1688pc']

    def to_db(self, records):
        for record in records:
            print("Saving records: ", record)
            self._table.upsert(record, ['ads_url'])
