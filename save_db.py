#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dataset


class Saver:

    def __init__(self):
        self._db = dataset.connect('mysql://root:mini08!@192.168.0.220:3306/1688?charset=utf8')
        self._table = self._db['1688pc_copy1']

    def to_db(self, records):
        for i, record in enumerate(records):
            print("    - Saving record #%i: %s" % (i, record))
            self._table.upsert(record, ['ads_url'])
