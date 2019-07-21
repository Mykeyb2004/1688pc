#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from logistics import UpdateLogistics

if __name__ == '__main__':
    print("Start to update logistics fee.")
    update = UpdateLogistics()
    update.update_db()
    print("Job is done.")
