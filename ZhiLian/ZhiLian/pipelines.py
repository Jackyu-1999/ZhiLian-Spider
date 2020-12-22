# -*- coding: utf-8 -*-


import csv



# CSV保存数据
class ZhilianPipeline(object):
    def __init__(self):
        print("开始爬取目标网站.........")
    
    def process_item(self, item, spider):
        with open('Zhilian.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
            fieldnames = ['职位名称', '公司名称', '工作城市', '薪资范围', '学历要求', '公司类型', '公司规模', '职位类别', '工作经验', '福利待遇']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(
                {'职位名称': item['poname'], '公司名称': item['coname'], '工作城市': item['city'], '薪资范围': item['providesalary'], '学历要求': item['degree'],
                 '公司类型': item['coattr'], '公司规模': item['cosize'], '职位类别': item['rank'], '工作经验': item['worktime'], '福利待遇': item['welfare']})

            return item
    
    def close_spider(self, spider):
            print("爬虫已经运行完毕.........")



















