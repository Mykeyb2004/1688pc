# Chrome部分设置
****
MD快捷键  
`Ctrl+Alt+O`: Preview Markup in Browser.  
`Ctrl+Alt+X`: Export Markup as HTML.  
`Ctrl+Alt+C`: Copy Markup as HTML.  
其他插件页面: <https://www.jianshu.com/p/aa30cc25c91b>

----
### 测试
[检测chrome状态](https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html)

### 改变目录执行权限
chmod 777 dir

### 可以修改环境变量，指定chromedriver的执行路径

### 启动chrome的参数（远程调试）
`chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"`

### 鼠标悬停设置
[鼠标悬停 hover](https://stackoverflow.com/
questions/8252558/is-there-a-way-to-perform-a-mouseover-hover-over-an-element-using-selenium-and/8261754)  
[另外可参考网址](https://stackoverflow.com/questions/19933914/selenium-python-hover-and-click-on-element)

源代码
```cpython
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

firefox = webdriver.Firefox()
firefox.get('http://foo.bar')
element_to_hover_over = firefox.find_element_by_id("baz")

hover = ActionChains(firefox).move_to_element(element_to_hover_over)
hover.perform()
```
### 调用已打开的浏览器
- cmd 运行命令`chrome.exe --remote-debugging-port=9222`  
- 打开一个浏览器，然后py代码里`chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")`添加一个这个Options。其它的代码不变  


### selenium等待特定元素加载完毕
`is_disappeared = WebDriverWait(driver, 8, 0.5, ignored_exceptions=TimeoutException).until(lambda x: x.find_element_by_id("id").is_displayed())`

等待页面加载完成，找到某个条件发生后再继续执行后续代码，如果超过设置时间检测不到则抛出异常  
`WebDriverWait(driver, timeout, poll_frequency=0.5, ignored_exceptions=None)`

——`driver`：WebDriver 的驱动程序(Ie, Firefox, Chrome 或远程)  
——`timeout`：最长超时时间，默认以秒为单位  
——`poll_frequency`：休眠时间的间隔（步长）时间，默认为 0.5 秒  
——`ignored_exceptions`：超时后的异常信息，默认情况下抛 `NoSuchElementException` 异常

`
is_disappeared = WebDriverWait(driver, 30, 1, (ElementNotVisibleException)).until_not(lambda x: x.find_element_by_id(“someId”).is_displayed())
`  

WebDriverWai()一般由 unit()或 until_not()方法配合使用:

——`until(method, message=’’)` 调用该方法提供的驱动程序作为一个参数，直到返回值不为 False。  
——`until_not(method, message=’’)` 调用该方法提供的驱动程序作为一个参数，直到返回值为 False。

```
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
driver=webdriver.Firefox()
driver.get()
WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("someId"))
```
* 通过检查某个元素是否被加载来检查是否登录成功，我认为当个黑盒子用就可以了。其中10的解释：10秒内每隔0.5毫秒扫描1次页面变化，直到指定的元素 *


----
### selenium webdriver三种等待方法
webdriver三种等待方法  

#### 使用WebDriverWait
```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait                            # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC           # available since 2.26.0
driver = webdriver.Firefox()
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))
finally:
    driver.quit()
```
`presence_of_element_located`可以替换为

`title_is`  
`title_contains`  
`presence_of_element_located`  
`visibility_of_element_located`  
`visibility_of`  
`presence_of_all_elements_located`  
`text_to_be_present_in_element`  
`text_to_be_present_in_element_value`  
`frame_to_be_available_and_switch_to_it`  
`invisibility_of_element_located`  
`element_to_be_clickable`   - it is Displayed and Enabled.  
`staleness_of`  
`element_to_be_selected`  
`element_located_to_be_selected`  
`element_selection_state_to_be`  
`element_located_selection_state_to_be`  
`alert_is_present`

`By.ID`中的ID可替换为`CLASS_NAME`, `CSS_SELECTOR`, `ID`, `LINK_TEXT`, `NAME`, `PARTIAL_LINK_TEXT`, `TAG_NAME`, `XPATH`

#### 隐式等待，相当于设置全局的等待，在定位元素时，对所有元素设置超时时间。

隐式等待使得WebDriver在查找一个Element或者Element数组时，每隔一段特定的时间就会轮询一次DOM，如果Element或数组没有马上被发现的话。默认设置是0。
一旦设置，这个隐式等待会在WebDriver对象实例的整个生命周期起作用。
```
from selenium import webdriver
driver = webdriver.Firefox()
driver.implicitly_wait(10)                      # seconds
driver.get(http://www.xxx.com)
myDynamicElement = driver.find_element_by_id("ElementID")
```
#### 强制等待
```
import time
time.sleep(10)
```

#### 使用python处理selenium中的xpath定位元素的模糊匹配问题
+ 用contains，寻找页面中style属性值包含有sp.gif这个关键字的所有div元素,其中@后面可以跟该元素任意的属性名。
`self.driver.find_element_by_xpath('//div[contains(@style,"sp.gif")]').click()`
+ 用start-with，寻找style属性以position开头的div元素,其中@后面可以跟该元素任意的属性名。
`self.driver.find_element_by_xpath('//div[start-with(@style,"position")]').click()`
+ 用Text，直接查找页面当中所有的退出二字，经常用于纯文字的查找。
`self.driver.find_element_by_xpath('//*[text()="退出"]').click()`
+ 用于知道超链接上显示的部分或全部文本信息
`self.driver.find_element_by_xpath('//a[contains(text(), "退出")]').click()`

#### 获取元素的html内容
`element.get_attribute('innerHTML')`

#### 获取元素的文本值
`element.get_attribute(‘textContent’)`

#### 导出python安装包环境
`pip freeze > requirements.txt`

#### 导入requirements文件
`pip install -r requirements.txt`