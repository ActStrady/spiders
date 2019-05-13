#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/13 9:58
# @Author : ActStrady@tom.com
# @FileName : douban_login.py
# @GitHub : https://github.com/ActStrady/spiders

"""
实现自动登录
主要有两种实现：1.利用session，传入data属性来做，如果有验证码则不能使用
             2.利用网站cookie来实现，传入cookies属性
"""

import requests
import util

# 登录地址
login_url = 'https://accounts.douban.com/j/mobile/login/basic'
# 请求头
header = util.HEADER


def login_session():
    """
    利用session来实现自动登录
    :return: session
    """
    # 表单数据
    form_data = {"ck": "",
                 "name": "13702059309",
                 "password": "qw147258369",
                 "remember": "true",
                 'ticket': ""}
    # 获取Session
    # 模拟登录
    session = requests.Session()
    # 模拟登录
    result = session.post(login_url, headers=header, data=form_data)
    status = result.json()['status']
    if status == 'success':
        print('登录成功')
    else:
        print('登录失败')
    return session


def login_cookie():
    """
    使用cookie实现自动登录
    :return: cookie字典
    """
    # 从文件读取cookie
    with open('../resources/douban_cookie.txt', encoding='utf-8') as f:
        cookie_str = f.readline()
    # 处理cookie
    cookie_list = cookie_str.split(';')
    # 将cookie封装为字典
    cookie_dict = dict()
    for cookie in cookie_list:
        key_value = cookie.strip().split('=')
        key = key_value[0]
        value = key_value[1]
        cookie_dict[key] = value
    return cookie_dict


if __name__ == '__main__':
    # session = login_session()
    # html = session.get('https://www.douban.com/people/196409571/notes', headers=header)
    # print(html.text)
    cookie_dict_ = login_cookie()
    html = requests.get('https://www.douban.com/people/196409571/notes', headers=header, cookies=cookie_dict_)
    # 如果打印的有 '都' 则成功
    print(html.text)
