#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 控制调试模式的开关
DEBUG = False
# DEBUG = True
# 数据表名称
TABLE = '1688pc' if not DEBUG else '1688pc_copy1'
# 数据库连接配置
CONNECTION = 'mysql://root:mini08!@192.168.0.220:3306/1688?charset=utf8'
