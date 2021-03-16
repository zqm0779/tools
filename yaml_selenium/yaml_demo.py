# -*- coding: utf-8 -*-
"""
@Time ： 2021/3/16
@Auth ： zhangqimin
@File ：yaml_demo.py
@IDE ：PyCharm

"""
import re
from time import sleep

import pytest
import yaml
from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By

#读取yaml的数据
def load_data(path):
    with open(path, encoding='utf-8') as f:
        result = yaml.safe_load(f)
        # print(result)
        return result

#测试数据   keyword: [appium,selenium]
def data_gen(data):
    res = []
    if isinstance(data, dict):
        # print(list(data.values()))
        length = len(list(data.values())[0])
        # print(length)
        for i in range(length):
            temp = []
            for value in data.values():
                temp.append(value[i])
            res.append(temp[0])
    print(f'res={res}')
    return res


class TestDemo:
    data_file = load_data("test_data.yaml")
    # print(data_file)
    #data-keyword
    test_data = data_gen(data_file['data'])
    # print(test_data)
    test_steps = data_file['steps']
    # print(test_steps)
    driver: WebDriver = None
    current_element: WebElement = None
    _var = {}

    # #todo: driver=none
    # def teardown_class(self):
    #     pass
    #     # self.driver.quit()

    # 测试数据的数据驱动
    # @pytest.mark.parametrize('path', ['test_data.yaml', 'test_data.yaml'])
    # todo: pytest hook机制
    @pytest.mark.parametrize('data', test_data)
    def test_search(self, data):
        # 测试步骤的数据驱动
        for step in self.test_steps:
            if isinstance(step, dict):
                #判断浏览器类型
                if 'webdriver' in step:
                    browser = str(step.get("webdriver").get("browser")).lower()
                    if browser == 'chrome':
                        self.driver = webdriver.Chrome()
                    elif browser == 'firefox':
                        self.driver = webdriver.Firefox()
                    else:
                        print(f"{self.driver} don't know which browser")

                    if self.driver is not None:
                        self.driver.implicitly_wait(10)
                #获取url地址
                if 'get' in step:
                    url = step.get('get')
                    self.driver.get(url)

                if 'find_element' in step:
                    if isinstance(step.get("find_element"), list):
                        by = step.get("find_element")[0]
                        locator = step.get("find_element")[1]
                    elif isinstance(step.get("find_element"), dict):
                        by = step.get("find_element")['by']
                        locator = step.get("find_element")['value']
                    if by == "css":
                        by = By.CSS_SELECTOR
                    print(by,locator)
                    current_element = self.driver.find_element(by, locator)
                #点击事件
                if 'click' in step:
                    current_element.click()
                #输入框输入数据
                if 'send_keys' in step:
                    #获得yaml参数化${data}
                    value = str(step.get("send_keys"))
                    # 判断value是否是变量 ${data}
                    value = self.replace(value, data)
                    # print(type(value))
                    # print(value)
                    current_element.send_keys(value.split("'"))
                #获取结果
                print(step.keys())
                if str(list(step.keys())[0]).startswith('get_a'):
                    key = list(step.values())[0]
                    if key == "text":
                        self._var["return"] = current_element.text
                        # print(self._var["return"])
                    else:
                        self._var["return"] = current_element.get_attribute(key)
                        print(self._var["return"])
                    print('-----------')
                    # print(self._var["return"])

                if 'var' in step:
                    # 追加新的变量数据
                    for k, v in dict(step.get("var")).items():
                        v = self.replace(v, data)
                        self._var[k] = v

                if 'assert_in' in step:
                    assert_data = list(step.values())[0]
                    sub = assert_data[0]
                    sub = self.replace(sub, data)
                    print(sub)
                    print(type(sub))
                    collection = assert_data[1]
                    print(collection)
                    collection = self.replace(collection, data)
                    print(type(collection))
                    print(sub in str(collection))
                    assert sub in str(collection)

        # driver=webdriver.Chrome()
        # driver.get('https://ceshiren.com/')
        # driver.find_element(By.ID, 'search-button').click()
        # driver.find_element(By.ID, 'search-term').send_keys(keyword)

    def replace(self, content, param=None):
        if isinstance(content, str):
            for k, v in self._var.items():
                if v is None:
                    v = ""
                content = content.replace(f'${{{k}}}', v)
            if param is not None:
                content = content.replace(str('${data}'), str(param))
        return content

if __name__ == '__main__':
    case = TestDemo()
    case.test_search(case.test_data)