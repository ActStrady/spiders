drop database if exists douban;
create database douban;

drop table if exists douban.info;
create table douban.info
(
    id        int auto_increment primary key comment '主键',
    name      varchar(255) not null comment '电影名',
    url       varchar(255) not null comment '详情链接',
    director  varchar(255) comment '导演',
    actor     varchar(255) comment '主演',
    star      varchar(255) not null comment '星级',
    grade     varchar(255) not null comment '评分',
    grade_num varchar(255) not null comment '评分人数',
     pic_url varchar(255) not null comment '电影图片地址'
) comment '豆瓣top250电影信息表';