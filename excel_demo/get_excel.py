# -*- coding: utf-8 -*-
"""
@Time ： 2021/3/16
@Auth ： zhangqimin
@File ：get_excel.py
@IDE ：PyCharm

"""
import xlrd
import os
'''读取Excel'''
'''
xlrd版本问题，导致报错：xlrd.biffh.XLRDError: Excel xlsx file; not supported
将xlrd的版本安装成1.2.0，详情见
https://www.cnblogs.com/xiaoqiangink/p/14144517.html
'''
def get_file_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = current_path + '\\' + "test_data" + '\\' + 'case.xlsx'
    print(file_path)
    return file_path

def get_data(filepath):
    all_case = []
    #打开excel文件
    file = xlrd.open_workbook(filepath)
    #获取excel的sheet名称
    sheet_name = file.sheets()[0]
    #获取sheet的行数
    nrows = sheet_name.nrows
    for i in range(1,nrows):
        all_case.append({"id": sheet_name.cell(i, 0).value,
                         'key': sheet_name.cell(i, 2).value,
                         'comment': sheet_name.cell(i,3).value,
                         'url': sheet_name.cell(i,4).value,
                         'name': sheet_name.cell(i,1).value,
                         'method': sheet_name.cell(i,5).value,
                         'assert': sheet_name.cell(i,6).value
                         })
    return all_case

if __name__ == '__main__':
    print(get_data(get_file_path()))