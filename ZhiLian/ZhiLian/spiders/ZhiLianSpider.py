# -*- coding: utf-8 -*-
import json
import time
import scrapy
from scrapy.spiders import CrawlSpider
from ZhiLian.items import ZhilianItem

# pageSize: 返回数据的数量，默认返回50条，最多返回90条
# pageNo: 翻页参数，默认为1
# cityId: 城市id，默认为-1，如：`北京` 的id为 `530`
# workExperience: 工作经验参数，默认为-1，如：`1-3年` 经验为 `0103`
# jobType: 职位类型id，默认为-1，如：`汽车销售` 为 `19000200150000`
#  education: 学历要求，默认为-1，如：`本科` 为 `4`
# companyType: 公司类型，默认为-1，如：`国企` 为 `1`
# companySize: 公司规模，默认为-1，如：`100-299人` 为 `3`


class ZhilianspiderSpider(scrapy.Spider):
    start = time.time()
    name = 'ZhiLianSpider'
    allowed_domains = ['zhaopin.com']
    # 构造城市名字典，利用字典的键值对形成映射关系
    city_list = {'北京': '530', '上海': '538', '广州': '763', '深圳': '765', '长沙': '749', '杭州': '653', '成都': '801', '厦门': '682'}

    city_name = input("请输入城市: ")
    city_id = city_list[city_name]
    # 构造职位类型字典
    job_list = {'销售/商务拓展': '19000000000000', '人事/行政/财务/法务': '14000000000000',
                '互联网/通信及硬件': '9000000000000', '运维/测试': '20000000000000', '视觉/交互/设计': '17000000000000',
                '运营/专业分析': '5000000000000', '产品/项目/高级管理': '3000000000000', '市场/品牌/公关': '16000000000000',
                '金融/保险': '12000000000000', '房地产/工程/建筑': '7000000000000', '物流/采购/供应链': '2000000000000',
                '生产制造/营运管理': '15000000000000', '农业/能源/环保': '21000000000000', '医疗/医美': '18000000000000',
                '教育/培训/科研': '11000000000000', '编辑/记者/翻译': '1000000000000', '影视传媒': '4000000000000',
                '商务服务/生活服务': '6000000000000', '管培生/非企业从业者': '8000000000000'
                }
    job_name = input("请输入职位类型: ")
    jod_id = job_list[job_name]
    # 拼接初始化Url

    start_urls = [
        "https://fe-api.zhaopin.com/c/i/jobs/searched-jobs?pageNo=1&pageSize=90&cityId=" + city_id + "&workExperience=0305&jobType=" + jod_id + "&education=4&companyType=-1"]

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
                # print(item)
                yield item

    end = time.time()
    print("本次爬取花费时间为：" + str(end - start))






