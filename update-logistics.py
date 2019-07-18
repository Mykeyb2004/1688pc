#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from logistic import UpdateLogistics

if __name__ == '__main__':
    update = UpdateLogistics()
    update.update_db()
    print("Job is done.")
