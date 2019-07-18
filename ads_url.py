#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class AdsUrl:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def get_url(self, ads_url):
        self.driver.get(ads_url)
        return self.driver.current_url
