#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import dataset
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import *
from utils import *


class Logistic:
    """
    从移动端页面中获取物流费
    """

    def __init__(self):
        chrome_options = Options()
        # 禁止下载图片
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # 禁止插件
        chrome_options.add_argument("--disable-plugins")
        # 开启实验性性功能，关闭部分selenium特征码
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        if not DEBUG:
            chrome_options.add_argument("--headless")
        self._driver = webdriver.Chrome(chrome_options=chrome_options)
        self._wait = WebDriverWait(self._driver, 3)
        # self._driver.implicitly_wait(10)
        print("Starting Webdriver...")

    def switch_tab(self):
        # 切换到分销或代发页面
        pattern = "//div[contains(@class,'J_Tab_List takla-tab-title-list')]/div[last()]"
        try:
            retail_tab = self._wait.until(EC.presence_of_element_located((By.XPATH, pattern)))
            retail_tab.click()
        except Exception:
            pass

    def get_cost(self, url):
        self._driver.get(url)
        self.switch_tab()

        pattern = "//div[@class='takla-wap-dpl-item is-small-item no-border-bottom detail-logistics-container']//div[@class='takla-item-content']/span[last()]/span[last()]"
        try:
            logistic_element = self._wait.until(EC.presence_of_element_located((By.XPATH, pattern)))
            logistic_cost = currency(logistic_element.get_attribute("innerHTML"))
        except Exception:
            # print("Logistic cost cannot be found.")
            logistic_cost = 0
        return logistic_cost

    def __del__(self):
        self._driver.close()
        print("Webdriver Shutdown")


class UpdateLogistics:
    """
    将物流费更新到数据库中
    """

    def __init__(self):
        self._db = dataset.connect(CONNECTION)
        self._table = self._db[TABLE]

    def update_db(self):
        sql = "SELECT id, url, logistics_cost FROM {0} WHERE logistics_cost is NULL".format(TABLE)
        records = self._db.query(sql)

        if not records:
            print("No links found.")
            return

        logistics = Logistic()
        for i, item in enumerate(records):
            if not item['url']:
                break
            url = mobile_url(get_id_from_url(item['url']))
            print("[#%d] Detecting link %s" % ((i + 1), url), end="\t")
            logistics_cost = logistics.get_cost(url)
            print(logistics_cost, end="\t")
            # 保存记录
            record = dict(id=item['id'], logistics_cost=logistics_cost)
            self.update_logistics_cost(record)
            if DEBUG and i >= 10:
                break
        del logistics

    def update_logistics_cost(self, record):
        self._table.update(record, ['id'])
        print("Saved.")
