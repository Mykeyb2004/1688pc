#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class Combiner:
    def __init__(self):
        self._product = []
        self.__product_name = []

    @property
    def product_name(self):
        return self.__product_name

    @product_name.setter
    def product_name(self, value):
        if not isinstance(value, list):
            raise ValueError("product_name is not list.")
        self.__product_name = value
