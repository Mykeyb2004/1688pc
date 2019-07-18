#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dataset
from config import *


class Saver:

    def __init__(self):
        self._db = dataset.connect(CONNECTION)
        self._table = self._db[TABLE]

    def to_db(self, records):
        for i, record in enumerate(records):
            print("    - Saving record #%i: %s" % (i, record))
            self._table.upsert(record, ['ads_url'])
