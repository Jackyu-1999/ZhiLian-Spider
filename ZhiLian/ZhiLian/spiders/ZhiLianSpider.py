# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.spiders import CrawlSpider
from ZhiLian.items import ZhilianItem


class ZhilianspiderSpider(scrapy.Spider):
    name = 'ZhiLianSpider'
    allowed_domains = ['zhaopin.com']
    edu_id = input(" 初中及以下: 9  高中:  7  中专/中技: 12 大专:  5  本科: 4  硕士: 3 博士: 1  MBA/EMBA: 10 -- 请输入学历类型ID: ")

    # 拼接初始化Url
    start_urls = [
        "https://fe-api.zhaopin.com/c/i/jobs/searched-jobs?pageNo=1&pageSize=90&cityId=682&workExperience=-1&jobType=-1&education=" + edu_id + "&companyType=-1"]

    cotype_list = ['国企: 1', '外商独资: 2', '代表处: 3', '合资: 4', '民营: 5', '股份制企业: 8', '上市公司: 9', '国家机关: 6', '事业单位: 10',
                   '银行: 11',
                   '医院: 12', '学校/下级学院: 13', '律师事务所: 14', '社会团体: 15', '港澳台公司: 16', '其它: 7']
    cosize_list = ['20人以下: 1', '20-99人: 2', '100-299人: 3', '300-499人: 8', '500-999人: 4', '1000-9999人: 5', '10000人以上: 6']
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS': 64
    }


    # 解析start_urls
    def parse(self, response):
        # 对应json数据中的data
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            # 没有数据
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for cotype in self.cotype_list:
                yield scrapy.Request(
                    url=str(response.url).replace('companyType=-1', f'companyType={cotype.split(": ")[1]}'),
                    dont_filter=True,
                    callback=self.parse_cotype
                )

    # 按公司类型解析
    def parse_cotype(self, response):
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for cosize in self.cosize_list:
                yield scrapy.Request(
                    url=str(response.url).replace('companySize=-1', f'companySize={cosize.split(": ")[1]}'),
                    dont_filter=True,
                    callback=self.parse_cosize
                )

    # 按公司规模解析
    def parse_cosize(self, response):
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for page in range(1, 4):
                yield scrapy.Request(
                    url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                    dont_filter=True,
                    callback=self.parse_result
                )

    # 对最终的结果进行解析
    def parse_result(self, response):
        item = ZhilianItem()
        datas = json.loads(response.text)
        try:
            data_list = datas['data']['list']
        except Exception:
            data_list = []

        if len(data_list) > 0:
            for data in data_list:
                item = {}
                # 职位名称
                item['poname'] = data['name']
                # 公司名称
                item['coname'] = data['company']
                # 工作城市
                item['city'] = data['workCity']
                # 薪资范围
                item['providesalary'] = data['salary']
                # 学历要求
                item['degree'] = data['education']
                # 公司类型
                item['coattr'] = data['property']
                # 公司规模
                item['cosize'] = data['companySize']
                # 职位类别
                item['rank'] = data['jobType']
                # 工作经验
                item['worktime'] = data['workingExp']
                # 福利待遇
                # 提取json数据中的value值，先转换为列表，再转换为字符串返回
                json_data = data['welfareLabel']
                json_list = []
                for i in json_data:
                    json_list.append(i['value'])
                temp_data = [str(k) for k in json_list]
                welfare_str = ','.join(temp_data)
                item['welfare'] = welfare_str
                print(item)
                yield item










