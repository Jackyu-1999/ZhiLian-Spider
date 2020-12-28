# -*- coding: utf-8 -*-
# pipelines文件内容，定义数据存储的方式，此处定义数据存储的逻辑，
# 可以将数据存储载MySQL数据库，MongoDB数据库，文件，CSV，Excel等存储介质中
# import csv
import pymongo

# 保存至MongoDB数据库
class ZhilianPipeline(object):
    def process_item(self, item, spider):
        con = pymongo.MongoClient("mongodb://localhost:27017")
        con = pymongo.MongoClient(host='localhost', port=27017)

        # 选择使用哪个数据库
        mydb = con['data']

        # 使用哪个集合
        myset = mydb['info']
        infomations = {'职位名称': item['poname'], '公司名称': item['coname'], '工作城市': item['city'], '薪资范围': item['providesalary'], '学历要求': item['degree'],
                         '公司类型': item['coattr'], '公司规模': item['cosize'], '职位类别': item['rank'], '工作经验': item['worktime'], '福利待遇': item['welfare']}

        myset.insert(infomations)
        return item













