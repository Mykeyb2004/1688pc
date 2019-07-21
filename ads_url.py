#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class AdsUrl:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # 根据操作系统指定不同的chromedriver
        if platform.system() == 'Windows':
            chrome_driver = os.path.abspath('.') + '\\chromedriver.exe'
        else:
            chrome_driver = "/usr/lib/chromium-browser/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)

    def get_url(self, ads_url):
        self.driver.get(ads_url)
        return self.driver.current_url
