#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/10 10:07
# @Author : ActStrady@tom.com
# @FileName : douban_spiders.py
# @GitHub : https://github.com/ActStrady/spiders
import os
import re
import requests
from urllib.request import urlopen
from lxml import etree

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/74.0.3729.131 Safari/537.36'}
# 电影数据列表
movie_info_list = list()
# 电影图片列表
movie_pic_list = list()


def page_movies_info(page):
    """
    获取豆瓣电影Top250一页的电影数据
    :param page: 页数
    :return: 本页电影数据列表
    """
    page_movies_info_list = list()
    # 获取html页面
    html = requests.get('https://movie.douban.com/top250?start={}'.format(page * 25), headers=header)

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


def recursion_movies(url):
    # 获取html页面
    html = requests.get(url, headers=header)

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
        # 图片url
        pic_url = movie_selector.xpath(".//img/@src")[0]

        # 保存信息
        movie_info = (name, url, director, actor, star, grade, grade_num)
        movie_pic = (name, pic_url)
        movie_info_list.append(movie_info)
        movie_pic_list.append(movie_pic)

    # 有下一页就递归获取
    next_selector = selector.xpath("//span[@class='next']/a/@href")
    if next_selector:
        next_url = 'https://movie.douban.com/top250' + next_selector[0]
        recursion_movies(next_url)
    return movie_info_list, movie_pic_list


def page_movies_pic(page):
    """
    获取页面的一页图片
    :param page: 页数
    :return: 本页的电影图片
    """
    page_movies_pic_list = list()
    # 获取html页面
    html = requests.get('https://movie.douban.com/top250?start={}'.format(page * 25), headers=header)

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
        page_movies_info_list = page_movies_info(i)
        for movie_info in page_movies_info_list:
            movies_info_list.append(movie_info)
    return movies_info_list


def all_movies_pic():
    """
    获取全部图片
    :return: 全部电影图片
    """
    movies_pic_list = list()
    for i in range(10):
        page_movies_pic_list = page_movies_pic(i)
        for movie_pic in page_movies_pic_list:
            movies_pic_list.append(movie_pic)
    return movies_pic_list


def save_to_file(path, data_list):
    """
    文件保存到本地
    :param : 数据列表
    """
    # 删掉文件
    if os.path.exists(path):
        os.remove(path)
    # 写入文件
    for movie in data_list:
        with open(path, 'a', encoding='utf-8') as f:
            movie_str = ','.join(movie) + '\n'
            f.write(movie_str)


def down_to_file(data_list):
    """
    数据下载到本地
    :param data_list: 数据列表
    """
    for data in data_list:
        name = data[0]
        image_url = data[1]
        image_type = re.findall('.*\\.(.*)', image_url)[0]
        with urlopen(image_url) as f_image:
            with open('../douban/pic/{}.{}'.format(name, image_type), 'wb') as f:
                f.write(f_image.read())


if __name__ == '__main__':
    # print(all_movies_info())
    # print(all_movies_pic())
    # save_to_file('../douban/info/movies_info.txt', all_movies_info())
    # save_to_file('../douban/info/movies_pic.txt', all_movies_pic())
    # down_to_file(all_movies_pic())
    movie_lists = recursion_movies('https://movie.douban.com/top250')
    save_to_file('../douban/info/movies_info.txt', movie_lists[0])
    save_to_file('../douban/info/movies_info.txt', movie_lists[1])
    down_to_file(movie_lists[1])
