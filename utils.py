#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import json


def currency(text, null_value=None):
    """
    提取货币数字
    :param text: 待处理字符串
    :param null_value: 若无数字则返回的值
    :return: 将最后一组数字转化为float型，若无数字返回指定缺省值
    """
    number = re.findall(r'-?\d+\.?\d*e?-?\d*?', text)
    # 查看是否有“万”字
    if text.find('万') > 0:
        million = 10000
    else:
        million = 1
    # 转化为数字
    if number:
        return round(float(number[-1]) * million, 2)
    else:
        return null_value


def percent(text, null_value=None):
    """
    :param text: 待处理字符串
    :param null_value: 若无数字则返回的值
    :return: 将最后一组数字转化为float型（百分数），若无数字返回指定缺省值
    """
    number = re.findall(r'-?\d+\.?\d*e?-?\d*?', text)
    if number:
        return round(float(number[-1]) / 100, 4)
    else:
        return null_value


def int_number(text, null_value=None):
    """
    :param text: 待处理字符串
    :param null_value: 若无数字则返回的值
    :return: 将最后一组数字转化为int型，若无数字返回指定缺省值
    """
    number = re.findall(r'-?\d+\.?\d*e?-?\d*?', text)
    if number:
        return int(number[-1])
    else:
        return null_value


def get_pc_url(url):
    """
    从长链接中获取短链接
    :param url: 待处理链接（通过“?”解析出该符号前部分的链接地址）
    :return: 返回短链接
    """
    urls = url.split('?')
    if urls:
        return urls[0]
    else:
        return None


def get_id_from_url(url):
    """
    获取商品id
    :param url: 形如 (https://detail.1688.com/offer/566047493935.html)
    :return: 返回id
    """
    url = url.split('/')[-1]
    pos = url.find('.')
    url = url[:pos]
    return url


def mobile_url(product_id):
    """
    通过id生成移动端商品链接
    :param product_id: 商品id
    :return: 移动端商品链接
    """
    return "https://m.1688.com/offer/{0}.htm".format(product_id)


def load_config(filename):
    """
    载入配置文件（JSON格式）
    :param filename: 文件路径和文件名
    :return: 配置参数的数组
    """
    config = json.load(open(filename, encoding='UTF-8'))
    return config
