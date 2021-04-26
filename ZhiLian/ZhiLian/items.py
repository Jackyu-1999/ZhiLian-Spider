# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item
from scrapy import Field



# 继承父类scrapy.Item的属性和方法，该类用于定义需要爬取数据的子段
class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # 职位名称
    poname = scrapy.Field()
    # 公司名称
    coname = scrapy.Field()
    # 工作城市
    city = scrapy.Field()
    # 薪资范围
    providesalary = scrapy.Field()
    # 学历要求
    degree = scrapy.Field()
    # 公司类型
    coattr = scrapy.Field()
    # 公司规模
    cosize = scrapy.Field()
    # 工作经验
    worktime = scrapy.Field()
    # 福利待遇
    welfare = scrapy.Field()







