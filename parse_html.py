#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class HtmlParser:

    def __init__(self, driver):
        self._driver = driver
        self._product_info = []

    def get_page_data(self):
        title_list = self.get_product_title()
        image_url_list = self.get_image_url()
        url_list = self.get_url()
        for i in range(len(title_list)):
            data = {
                'title': title_list[i],
                'url': url_list[i],
                'image_url': image_url_list[i]
            }
            self._product_info.append(data)
        for item in self._product_info:
            print(item)

    def get_product_title(self):
        # 获取商品名称
        print("get_product_title")
        title_list = []
        url_list = []
        product_title_ele = self._driver.find_elements_by_xpath("//li[starts-with(@id, 'offer')]/div[2]/div[4]")
        for i, item in enumerate(product_title_ele):
            product_name_and_ads = item.text.split('\n')
            title_list.append(product_name_and_ads[-1])
            href = item.find_element_by_xpath(".//a").text  # get_attribute('href')
            url_list.append(href)
        return title_list

    def get_image_url(self):
        # 获取商品图片链接
        print("get_image_url")
        image_url_list = []
        product_images = self._driver.find_elements_by_xpath("//li[starts-with(@id, 'offer')]/div[2]/div[1]/a/img")
        for item in product_images:
            image_url_list.append(item.get_attribute('src'))
        return image_url_list

    def get_url(self):
        print("get_url")
        url_list = []
        url_ele = self._driver.find_elements_by_xpath("//li[starts-with(@id, 'offer')]/div[2]/div[4]/a")
        for item in url_ele:
            url_list.append(item.get_attribute('href'))
        return url_list

    def get_prices(self):
        # 获取批发销售条件
        conditions = self._driver.find_elements_by_xpath("//li[starts-with(@id, 'offer')]//div[contains\
            (@class,'s-widget-offershopwindowdealinfo sm-offer-dealInfo sm-offer-dealInfo')]")
        for i, item in enumerate(conditions):
            prices = item.find_elements_by_xpath(".//span/*[@title]")
            for price in prices:
                price_parts = price.get_attribute('title')
                print(price_parts)
            print("---")
        print(len(conditions))
