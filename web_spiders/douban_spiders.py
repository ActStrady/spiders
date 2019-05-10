#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/10 10:07
# @Author : ActStrady@tom.com
# @FileName : douban_spiders.py
# @GitHub : https://github.com/ActStrady/spiders
import os
import re

import requests
from lxml import etree


def page_movies_info(page):
    """
    获取豆瓣电影Top250一页的电影数据
    :param page: 页数
    :return: 本页电影数据列表
    """
    page_movies_info_list = list()
    # 获取html页面
    html = requests.get('https://movie.douban.com/top250?start={}'.format(page * 25))

    # 解析
    selector = etree.HTML(html.text)
    movies_selector = selector.xpath("//ol[@class='grid_view']/li")

    # 获取电影信息内容
    for movie_selector in movies_selector:
        # 电影名
        name = movie_selector.xpath(".//div[@class='hd']/a/span[1]/text()")[0]
        # url
        url = movie_selector.xpath(".//div[@class='hd']/a/@href")[0]
        # 导演和主演
        director_actor = movie_selector.xpath(".//div[@class='bd']/p[1]/text()")[0]
        # 使用正则
        director = re.findall('导演: (.*?) ', director_actor)[0]
        actor_list = re.findall('主演: (.*?) ', director_actor)
        if actor_list:
            actor = actor_list[0]
        else:
            actor = ''
        # 星数
        star = movie_selector.xpath(".//div[@class='star']/span[1]/@class")[0]
        # 评分
        grade = movie_selector.xpath(".//div[@class='star']/span[@class='rating_num']/text()")[0]
        # 评价人数
        grade_num_str = movie_selector.xpath(".//div[@class='star']/span[last()]/text()")[0]
        grade_num = re.findall('\\d*', grade_num_str)[0]
        movie_info = (name, url, director, actor, star, grade, grade_num)
        page_movies_info_list.append(movie_info)
    return page_movies_info_list


def page_movies_pic(page):
    page_movies_pic_list = list()
    # 获取html页面
    html = requests.get('https://movie.douban.com/top250?start={}'.format(page * 25))

    # 解析
    selector = etree.HTML(html.text)
    movies_selector = selector.xpath("//ol[@class='grid_view']/li")
    for movie_selector in movies_selector:
        url = movie_selector.xpath(".//img/@src")[0]
        name = movie_selector.xpath(".//img/@alt")[0]
        movie_pic = (name, url)
        page_movies_pic_list.append(movie_pic)
    return page_movies_pic_list


def all_movies_info():
    """
    获取豆瓣电影Top250全部电影信息
    :return: 全部电影数据列表
    """
    movies_info_list = list()
    for i in range(10):
        # 获取每页电影
        page_movies_info_list = page_movies_info(i)
        for movie_info in page_movies_info_list:
            movies_info_list.append(movie_info)
    return movies_info_list


def all_movies_data(type):
    movies_pic_list = list()
    for i in range(10):
        # 获取每页电影
        page_movies_list = page_movies_info(i)
        for movie in page_movies_list:
            movies_pic_list.append(movie)
    return movies_pic_list


def save_to_file(path, data_list, mode):
    """
    保存到本地
    :param : 数据列表
    :return:
    """
    # 删掉文件
    if os.path.exists(path):
        os.remove(path)
    # 写入文件
    for movie in data_list:
        with open(path, mode, encoding='utf-8') as f:
            movie_str = ','.join(movie) + '\n'
            f.write(movie_str)


if __name__ == '__main__':
    print(all_movies_info())
    save_to_file('../douban/info/movies.txt', all_movies_info())
    print(page_movies_pic(0))
