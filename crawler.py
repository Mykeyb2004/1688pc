#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


class Crawler:
    # container_pattern = ""
    _page_counts = 0
    _current_page = 0

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
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
        for item in containers:
            hover = ActionChains(self.driver).move_to_element(item)
            hover.perform()
            sleep(delay)
        print("商品数：", len(containers))

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

    def crawl_all_pages(self):
        for i in range(self._current_page, self._page_counts):
            print(i)
            self.scroll_page()
            sleep(6)
