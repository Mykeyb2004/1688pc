#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import re


class HtmlParser:

    def __init__(self, driver):
        self._driver = driver

    def get_page_data(self):
        # 获取整个页面上的数据
        product_info = []  # 组合后的页面全部数据
        containers = self._driver.find_elements_by_xpath("//li[starts-with(@id, 'offer')]/div[2]")  # 商品信息元素框
        hovers = self._driver.find_elements_by_xpath(
            "//li[starts-with(@id, 'offer')]//div[contains(@class,'imgofferresult-hoverBlock')]")  # 浮动信息元素框

        if len(containers) != len(hovers):
            raise ValueError("商品元素框数与浮动信息元素框数不一致，检查是否有未定位或未展现的浮动元素框（内含价格及货描等指标）。")

        if not containers:
            print("未找到商品信息元素")
            return None
        if not hovers:
            print("为找到浮动信息元素（货描等指标）")
            return None

        for i in range(len(containers)):
            print("Parsing product %d." % (i + 1))
            title = self.get_product_title(containers[i])
            image_url = self.get_image_url(containers[i])
            url = self.get_url(containers[i])
            supplier, is_niu, years = self.get_supplier_info(containers[i])
            amount_30 = self.get_amount_30(containers[i])
            rebuy, model = self.get_rebuy_and_model(containers[i])
            price1, condition1, price2, condition2, price3, condition3 = self.get_prices(hovers[i])
            desc, response, delivery = self.get_indicators(hovers[i])
            # 组合数据字段
            data = {
                'title': title,
                'image_url': image_url,
                'url': url,
                'supplier': supplier,
                'is_niu': is_niu,
                'years': years,
                'amount_30': amount_30,
                'rebuy': rebuy,
                'model': model,
                'price1': price1,
                'condition1': condition1,
                'price2': price2,
                'condition2': condition2,
                'price3': price3,
                'condition3': condition3,
                'desc': desc,
                'response': response,
                'delivery': delivery
            }
            product_info.append(data)
        for item in product_info:
            print(item)

    @staticmethod
    def get_product_title(container):
        # 获取商品名称（含有“广告”字样）
        element = container.find_element_by_xpath(".//div[4]").text.split('\n')
        title = element[-1]
        return title

    @staticmethod
    def get_image_url(container):
        # 获取商品图片链接
        element = container.find_element_by_xpath(".//div[1]/a/img")
        image_url = element.get_attribute('src')
        return image_url

    @staticmethod
    def get_url(container):
        # 获取商品链接
        elements = container.find_elements_by_xpath(".//div[4]/a")
        url = elements[-1].get_attribute('href')
        return url

    @staticmethod
    def get_supplier_info(container):
        # 获取供应商名称
        element = container.find_element_by_xpath(".//div[5]/a")
        supplier = element.text

        supplier_qualification_eles = container.find_elements_by_xpath(".//div[5]/span")
        is_niu = False
        years = None
        if len(supplier_qualification_eles) == 0:
            is_niu = False
            years = None
        if len(supplier_qualification_eles) == 1:
            is_niu = False
            years = supplier_qualification_eles[0].find_element_by_xpath(".//a").text
        if len(supplier_qualification_eles) == 2:
            is_niu = True
            years = supplier_qualification_eles[0].find_element_by_xpath(".//a").text
        return supplier, is_niu, years

    @staticmethod
    def get_amount_30(container):
        # 获取30天内成交金额
        elements = container.find_elements_by_xpath(".//div[3]/span")
        if len(elements) > 1:
            amount_30 = elements[-1].get_attribute('title')
        else:
            amount_30 = None
        return amount_30

    @staticmethod
    def get_rebuy_and_model(container):
        # 获取回头率及经营模式
        rebuy = None
        model = None
        rebuy_elements = container.find_elements_by_xpath(".//div[6]/span")
        model_element = container.find_element_by_xpath(".//div[6]/i")
        if rebuy_elements:
            rebuy = rebuy_elements[-1].text
        if model_element:
            model = model_element.text
        return rebuy, model

    @staticmethod
    def get_prices(hover):
        # 获取批发销售条件
        price = [None] * 3
        condition = [None] * 3
        price_elements = hover.find_elements_by_xpath(".//div[contains\
            (@class,'s-widget-offershopwindowdealinfo sm-offer-dealInfo sm-offer-dealInfo')]/span/*[@title]")
        for i, item in enumerate(price_elements):
            if (i % 2) == 0:  # 偶数
                price[round(i / 2)] = item.get_attribute('title')
            else:  # 奇数
                condition[round(i / 3)] = item.get_attribute('title')
        return price[0], condition[0], price[1], condition[1], price[2], condition[2]

    @staticmethod
    def get_indicators(hover):

        def sign(text):
            if text.startswith('高于'):
                return 1
            if text.startswith('低于'):
                return -1

        def percent(text):
            return float(re.findall(r'-?\d+\.?\d*e?-?\d*?', text)[-1]) / 100

        indicator_elements = hover.find_elements_by_xpath(".//div[contains(@class,'sm-offer-bsr-row')]/span")
        if not indicator_elements:
            print("没有数据")
            return None, None, None

        indicator = []
        for i, item in enumerate(indicator_elements):
            indicator.append(item.get_attribute("innerHTML"))
        # 货描、响应、发货
        desc = sign(indicator[1]) * percent(indicator[2])
        response = sign(indicator[4]) * percent(indicator[5])
        delivery = sign(indicator[7]) * percent(indicator[8])
        return desc, response, delivery
