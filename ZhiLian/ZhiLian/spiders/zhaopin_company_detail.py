# -*- coding: utf-8 -*-
import json
import re
import time
import js2py
import scrapy


class ZhaopinCompanyDetailSpider(scrapy.Spider):
    name = 'zhaopin_company_detail'
    allowed_domains = ['zhaopin.com']
    start_urls = [
        'http://company.zhaopin.com/ACS%E5%A4%A7%E8%BF%9E%E8%B6%85%E8%83%9C%E4%BF%A1%E6%81%AF%E6%9C%8D%E5%8A%A1%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8_CC292937512.htm',
        'http://company.zhaopin.com/APC%E5%93%81%E7%89%8C%E4%BC%A0%E6%92%AD%E6%9C%BA%E6%9E%84_CC186956123.htm',
        'http://company.zhaopin.com/BUREAU+VERITAS+%E5%BF%85%E7%BB%B4%E5%9B%BD%E9%99%85%E6%A3%80%E9%AA%8C%E9%9B%86_CC000617847.htm',
        'http://company.zhaopin.com/CC000001066.htm', 'http://company.zhaopin.com/CC000019623.htm',
        'http://company.zhaopin.com/CC000021844.htm', 'http://company.zhaopin.com/CC000022144.htm',
        'http://company.zhaopin.com/CC000067551D90250047000.htm',
        'http://company.zhaopin.com/CC000067551D90250049000.htm',
        'http://company.zhaopin.com/CC000067551D90250050000.htm']

    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'RETRY_HTTP_CODES': [301],
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'LOG_LEVEL': 'INFO'
    }
    count = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=True,
                meta={'url': url}
            )

    def get_token(self, arg1):
        _0x4e08d8 = "3000176000856006061501533003690027800375"

        _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9,
                     0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19,
                     0xd,
                     0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a,
                     0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c,
                     0x22, 0x25, 0xc, 0x24]
        _0x4da0dc = [''] * 40
        _0x12605e = ''
        for _0x20a7bf in range(0, len(arg1)):
            _0x385ee3 = arg1[_0x20a7bf]
            for _0x217721 in range(0, len(_0x4b082b)):
                if _0x4b082b[_0x217721] == _0x20a7bf + 0x1:
                    _0x4da0dc[_0x217721] = _0x385ee3
        _0x12605e = ''.join(_0x4da0dc)
        _0x23a392 = _0x12605e

        token_js = """
                function get_token(_0x4e08d8, _0x23a392) {
                    var _0x5a5d3b = '';
                    for (var _0xe89588 = 0x0; _0xe89588 < _0x23a392["length"] && _0xe89588 < _0x4e08d8["length"]; _0xe89588 += 0x2) {
                        var _0x401af1 = parseInt(_0x23a392["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);
                        var _0x105f59 = parseInt(_0x4e08d8["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);
                        var _0x189e2c = (_0x401af1 ^ _0x105f59)["toString"](0x10);
                        if (_0x189e2c["length"] == 0x1) {
                            _0x189e2c = '\x30' + _0x189e2c;
                        }
                        _0x5a5d3b += _0x189e2c;
                    }
                    return _0x5a5d3b
                }
                """
        f = js2py.eval_js(token_js)
        return f(_0x4e08d8, _0x23a392)

    def parse(self, response):
        try:
            arg1 = re.findall(re.compile(r"var arg1='(.*?)';", re.S), response.text)[0]
        except Exception:
            try:
                arg1 = re.search("arg1='([^']+)'", response.text).group(1)
            except Exception:
                arg1 = ''
        if arg1 != '':
            token = self.get_token(arg1)
            yield scrapy.Request(
                url=response.url,
                headers={"Cookie": f'acw_sc__v2={token}; '},
                callback=self.parse_detail,
                dont_filter=True
            )

    def parse_detail(self, response):
        if 'arg1' in response.text:
            yield scrapy.Request(
                url=response.url,
                dont_filter=True,
                callback=self.parse
            )
        else:
            title = response.xpath('//div[@class="base-info__title"]/h1/text()')
            if title:
                json_data = re.findall(re.compile(r'<script>__INITIAL_STATE__=(.*?)</script>', re.S), response.text)[0]
                data = json.loads(json_data)
                if data['companyDetail']:
                    item = {}
                    # 公司唯一id
                    item['cocode'] = data['companyDetail']['companyBase']['companyNumber']
                    # 城市
                    item['city'] = data['companyDetail']['companyBase']['cityName']
                    # 地址
                    item['address'] = data['companyDetail']['companyBase']['address']
                    # 公司描述
                    item['description'] = str(data['companyDetail']['companyBase']['companyDescription']).replace(
                        '<div>', '').replace('</div>', '').replace('\n', '').replace('<p>', '').replace('</p>',
                                                                                                        '').replace(
                        '<br>', '').replace('&nbsp;', '').strip().replace(' ', '').replace('<li>', '').replace('</li>',
                                                                                                               '').replace(
                        '<ul>', '').replace('</ul>', '')
                    # 公司logo
                    item['logo'] = data['companyDetail']['companyBase']['companyLogo']
                    # 公司名称
                    item['coname'] = data['companyDetail']['companyBase']['companyName']
                    # 公司性质
                    item['nature'] = data['companyDetail']['companyBase']['property']
                    # 公司规模
                    item['cosize'] = data['companyDetail']['companyBase']['companySize']
                    # 公司类型
                    item['indtype'] = data['companyDetail']['companyBase']['industry']
                    item['company_url'] = response.url
                    # 批次
                    item['batch'] = time.strftime("%Y-%m", time.localtime())
                    # 插入时间
                    item['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['origin'] = '智联招聘'
                    item['status'] = 1
                    print(item)
                elif data['companyData']:
                    # 校园招聘
                    item = {}
                    # 公司唯一id
                    item['cocode'] = data['companyData']['AccountNumber']
                    # 城市
                    item['city'] = data['companyData']['CityName']
                    # 地址
                    item['address'] = data['companyData']['CompanyAddress']
                    # 公司描述
                    item['description'] = str(data['companyData']['CompanyDescription']).replace('<div>', '').replace(
                        '</div>', '').replace('\n', '').replace('<p>', '').replace('</p>', '').replace('<br>',
                                                                                                       '').replace(
                        '&nbsp;', '').strip().replace(' ', '').replace('<li>', '').replace('</li>', '').replace('<ul>',
                                                                                                                '').replace(
                        '</ul>', '')
                    # 公司logo
                    item['logo'] = data['companyData']['CompanyLogo']
                    # 公司名称
                    item['coname'] = data['companyData']['CompanyName']
                    # 公司性质
                    item['nature'] = data['companyData']['CompanyNature']
                    # 公司规模
                    item['cosize'] = data['companyData']['CompanySize']
                    # 公司类型
                    item['indtype'] = data['companyData']['Industry']
                    item['company_url'] = response.url
                    # 批次
                    item['batch'] = time.strftime("%Y-%m", time.localtime())
                    # 插入时间
                    item['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                       time.localtime())
                    item['origin'] = '智联招聘'
                    item['status'] = 1
                    print(item)
                else:
                    with open('extra.txt', 'a', encoding='utf8') as f:
                        f.write(response.url)
                        f.write('\n')
                        f.close()
            else:
                if self.count < 10:
                    self.count += 1
                    time.sleep(1)
                    print(f'正在尝试第{self.count}次重新请求,url:{response.url}')
                    yield scrapy.Request(
                        url=response.url,
                        dont_filter=True,
                        callback=self.parse
                    )
                else:
                    self.count = 0



