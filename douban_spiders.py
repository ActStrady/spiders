#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/10 10:07
# @Author : ActStrady@tom.com
# @FileName : douban_spiders.py
# @GitHub : https://github.com/ActStrady/spiders
import requests
from lxml import etree


def all_movies():
    movies = list()
    for i in range(10):
        # 获取html页面
        html = requests.get('https://movie.douban.com/top250?start={}'.format(i * 25))
        # 解析
        selector = etree.HTML(html.text)
        page_movies(selector, movies)
    return movies


def page_movies(selector, movies):
    movies_selector = selector.xpath("//ol[@class='grid_view']/li")
    # 电影列表

    for movie_selector in movies_selector:
        # 电影名
        name = movie_selector.xpath(".//div[@class='hd']/a/span[1]/text()")[0]
        # url
        url = movie_selector.xpath(".//div[@class='hd']/a/@href")[0]
        # 导演和主演
        director_actor = movie_selector.xpath(".//div[@class='bd']/p[1]/text()")[0]
        if '主演: ' in director_actor.split('导演: ')[1]:
            director = director_actor.split('导演: ')[1].split('主演: ')[0].strip('\xa0\xa0\xa0')
            actor = director_actor.split('导演: ')[1].split('主演: ')[1]
        else:
            director = director_actor.split('导演: ')[1].split('主演: ')[0].split('\xa0')[0]
            actor = ''
        # 星数
        star = movie_selector.xpath(".//div[@class='star']/span[1]/@class")[0]
        # 评分
        grade = movie_selector.xpath(".//div[@class='star']/span[@class='rating_num']/text()")[0]
        # 评价人数
        grade_num = movie_selector.xpath(".//div[@class='star']/span[last()]/text()")[0].split('人评价')[0]
        movie = (name, url, director, actor, star, grade, grade_num)
        movies.append(movie)


def save_to_file(movies):
    for movie in movies:
        with open('douban/movies.txt', 'a', encoding='utf-8') as f:
            movie_str = ','.join(movie) + '\n'
            f.write(movie_str)


if __name__ == '__main__':
    print(all_movies())
    save_to_file(all_movies())
