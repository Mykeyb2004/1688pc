#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import platform
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from parse_html import HtmlParser
from save_db import Saver
from config import *


class Crawler:
    _page_counts = 0
    _current_page = 0

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # 根据操作系统指定不同的chromedriver
        if platform.system() == 'Windows':
            chrome_driver = os.path.abspath('.') + '\\chromedriver.exe'
        else:
            chrome_driver = "/usr/lib/chromium-browser/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        self.driver.implicitly_wait(5)
        self.switch_to_1688()
        self._page_counts = int(self.driver.find_element_by_xpath("//em[contains(@class,'fui-paging-num')]").text)
        self._current_page = int(self.driver.find_element_by_xpath("//a[contains(@class,'fui-current')]").text)

    @property
    def page_counts(self):
        return self._page_counts

    @property
    def current_page(self):
        return self._current_page

    def switch_to_1688(self):
        """
        自动切换到1688网站的窗口
        :return:
        """
        handles = self.driver.window_handles  # 获取全部窗口句柄
        for handle in handles:
            self.driver.switch_to.window(handle)
            if str(self.driver.current_url).startswith('https://s.1688.com/'):
                break

    def hover_all(self, delay=0.5):
        """
        鼠标遍历悬停所有商品
        :param delay: 鼠标悬停时长
        :return:
        """
        containers = self.driver.find_elements_by_xpath('.//div[@class="imgofferresult-mainBlock"]')
        for i, item in enumerate(containers):
            hover = ActionChains(self.driver).move_to_element(item)
            hover.perform()
            if DEBUG and i > 10:
                break
            sleep(delay)

    def goto_page_bottom(self, scroll_times=3, delay=1.5):
        """
        滚动到页面底部，直到该页面上所有商品均已展现
        :param scroll_times: 尝试滚动次数
        :param delay: 滚动延时
        :return:
        """
        for i in range(scroll_times):
            containers = self.driver.find_elements_by_xpath('.//div[@class="imgofferresult-mainBlock"]')
            hover = ActionChains(self.driver).move_to_element(containers[-1])
            hover.perform()
            sleep(delay)

    def scroll_page(self):
        """
        翻到下一页
        :return:
        """
        next_page = self.driver.find_element_by_link_text('下一页')
        if next_page.is_enabled():
            next_page.click()

    def crawl_pages(self):
        parser = HtmlParser(self.driver)
        save = Saver()

        run_times = 0
        for i in range(self._current_page, self._page_counts + 1):
            run_times += 1
            print("Preparing to parse page #%d" % i)

            # 探测网络是否正常展示数据，如果没有则刷新数据
            self.refresh()

            # 刷新页面到底部
            print("  Refresh current page.")
            self.goto_page_bottom()

            # 悬停每个商品上，获取价格数据
            print("  Hover current page.")
            self.hover_all(0.5)

            # 解析页面数据
            print("  Parse current page.  [{0}/{1}]".format(i, self._page_counts + 1))
            records = parser.get_page_data()

            # 保存记录
            print("Saving to the database.")
            save.to_db(records)

            if DEBUG and run_times >= 1:
                break

            print("Scroll to the next page.")
            self.scroll_page()

            print("Wait and delay.")
            sleep(6)

    def refresh(self):
        # 若出现“网络出错，请刷新重试”,则点击重试
        try:
            retry = self.driver.find_element_by_link_text('刷新')
            if retry.is_enabled():
                retry.click()
        except NoSuchElementException:
            return
