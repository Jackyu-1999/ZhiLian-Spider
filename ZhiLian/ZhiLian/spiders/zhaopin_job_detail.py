# -*- coding: utf-8 -*-
# js2py库解密js代码
import re
import time
import js2py
import scrapy


class ZhaopinJobDetailSpider(scrapy.Spider):
    name = 'zhaopin_job_detail'
    # 允许爬取的域名
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://jobs.zhaopin.com/CC136280221J00483469007.htm',
                  'https://jobs.zhaopin.com/CC120989516J00443800608.htm',
                  'https://jobs.zhaopin.com/CC131324087J00265688011.htm',
                  'https://jobs.zhaopin.com/CC134085358J00470564408.htm',
                  'https://jobs.zhaopin.com/CC131486150J00316656707.htm',
                  'https://jobs.zhaopin.com/CC135627165J00618076005.htm',
                  'https://jobs.zhaopin.com/CC136050877J00441607308.htm',
                  'https://jobs.zhaopin.com/CC133205188J00450153407.htm',
                  'https://jobs.zhaopin.com/366572789250042.htm',
                  'https://jobs.zhaopin.com/CC136549678J00474522108.htm']

    count = 0
    # 自定义设置
    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 5,
        # 'DOWNLOAD_DELAY': 0.8,
        # 日志级别
        'LOG_LEVEL': 'INFO',
        # 用来控制当接收到的response头信息中的content-length和内容不匹配所采取的操作
        # 设置为false，时，校验未通过的response将被忽略
        'DOWNLOAD_FAIL_ON_DATALOSS': False
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                # 回调给parse函数
                callback=self.parse,
                # 不要过滤
                dont_filter=True,
                meta={'url': url}
            )

    # 通过js解密获取访问令牌
    def get_token(self, arg1):
        # 混淆变量
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
        # 计算token_js中的字符串，并执行其中的的 JavaScript代码
        f = js2py.eval_js(token_js)
        return f(_0x4e08d8, _0x23a392)

    # 解析函数
    def parse(self, response):
        if '滑动验证页面' in response.text:
            self.logger.warning(f'封禁IP：{response.meta.get("url")}')
        else:
            try:
                arg1 = re.search("arg1='([^']+)'", response.text).group(1)
            except:
                try:
                    arg1 = re.findall(re.compile(r"var arg1='(.*?)';", re.S), response.text)[0]
                except Exception:
                    arg1 = ''
            # 进一步判断关键字'xiaoyuan'是否存在于响应的url中，再通过回调分别交给负责解析校招和社招的函数进行解析处理
            if arg1:
                token = self.get_token(arg1)
                if 'xiaoyuan' in response.url:
                    # 校园招聘
                    yield scrapy.Request(
                        url=response.url,
                        headers={"Cookie": f'acw_sc__v2={token}; '},
                        callback=self.parse_campus,
                        dont_filter=True,
                        meta={'url': response.meta.get('url'), 'handle_httpstatus_list': [404]}
                    )
                else:
                    # 社会招聘
                    yield scrapy.Request(
                        url=response.url,
                        headers={"Cookie": f'acw_sc__v2={token}; '},
                        dont_filter=True,
                        callback=self.parse_detail,
                        meta={'url': response.meta.get('url'), 'handle_httpstatus_list': [404]}
                    )

    #  社招解析
    def parse_detail(self, response):
        # 判断状态码
        if response.status in (404,):
            if self.count < 3:
                yield scrapy.Request(
                    url=response.meta.get('url'),
                    callback=self.parse,
                    dont_filter=True,
                    meta={'url': response.meta.get('url')}
                )
                self.count += 1
            else:
                self.count = 0
                self.logger.warning('页面不存在：{}!!!'.format(response.meta.get('url')))

        # 通过判断arg1有没有出现在响应内容中，来决定是否回调给parse去解析
        elif 'arg1' in response.text:
            yield scrapy.Request(
                url=response.url,
                dont_filter=True,
                callback=self.parse,
                meta={'url': response.meta.get('url')}
            )

        # 出现滑动验证说明被封ip了
        elif '滑动验证页面' in response.text:
            self.logger.warning(f'封禁IP：{response.meta.get("url")}')

        # 上诉情况都没有发生则代表成功拿到数据，开始用xpath查找所需信息
        else:
            self.count = 0
            poname = response.xpath('//h3[@class="summary-plane__title"]/text()').get()
            providesalary = response.xpath('//span[@class="summary-plane__salary"]/text()').get()
            pcount = str(response.xpath('//ul[@class="summary-plane__info"]/li[last()]/text()').get()).replace('招',
                                                                                                               '').replace(
                '人', '')
            address = response.xpath('//span[@class="job-address__content-text"]/text()').get()
            skill = response.xpath('//div[@class="describtion__skills-content"]//text()').extract()
            if skill:
                skills = '|'.join(response.xpath('//div[@class="describtion__skills-content"]//text()').extract())
            else:
                skills = ''
            # 职位亮点/福利
            wel = response.xpath('//div[@class="highlights__content"]/span/text()').extract()
            if wel:
                welfare = '|'.join(response.xpath('//div[@class="highlights__content"]/span/text()').extract())
            else:
                welfare = ''
            # 职位描述
            jd = ''.join(
                response.xpath('//div[@class="describtion__detail-content"]/div//text()').extract()).replace(' ',
                                                                                                             '').replace(
                '\xa0', '')
            if jd == '':
                jd = ''.join(response.xpath('//div[@class="describtion__detail-content"]/p//text()').extract()).replace(
                    ' ', '').replace('\xa0', '')
                if jd == '':
                    jd = ''.join(
                        response.xpath('//div[@class="describtion__detail-content"]//text()').extract()).replace(' ',
                                                                                                                 '').replace(
                        '\xa0', '')
            city = '-'.join(response.xpath('//ul[@class="summary-plane__info"]/li[1]//text()').extract())
            # 经验要求
            exp = response.xpath('//ul[@class="summary-plane__info"]/li[2]/text()').get()
            # 学历要求
            edu = response.xpath('//ul[@class="summary-plane__info"]/li[3]/text()').get()
            # 更新时间
            # try:
            update_time = str(re.findall(re.compile(r'publishTime":"(.*?)"', re.S), response.text)[0]).split(' ')[0]
            # except Exception:
            #     update_time = re.findall(re.compile(r'发布时间(.*?)</span>.*?>(.*?)</span>', re.S), response.text)[0]
            # 时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 批次
            batch = time.strftime("%Y-%m", time.localtime())

            item = {}
            # 将所得信息存放至列表
            item['job_url'] = response.url
            item['poname'] = poname
            item['providesalary'] = providesalary
            item['city'] = city
            item['exp'] = exp
            item['edu'] = edu
            item['pcount'] = pcount
            item['update_time'] = update_time
            item['address'] = address
            item['welfare'] = welfare
            item['skills'] = skills
            item['jd'] = jd
            item['potype'] = '全职'
            item['created_at'] = created_at
            item['batch'] = batch
            item['recruitment_type'] = '社会招聘'
            item['origin'] = '智联招聘'
            item['status'] = 3
            print(item)


    #  校招解析
    def parse_campus(self, response):
        '''
        校园招聘职位详情，不封IP
        :param response: 响应结果
        :return: 职位详情
        '''
        if response.status in (404,):
            if self.count < 3:
                yield scrapy.Request(
                    url=response.meta.get('url'),
                    callback=self.parse,
                    dont_filter=True,
                    meta={'url': response.meta.get('url')}
                )
                self.count += 1
            else:
                self.count = 0
                self.logger.warning('页面不存在：{}!!!'.format(response.meta.get('url')))
        elif 'arg1' in response.text:
            yield scrapy.Request(
                url=response.url,
                dont_filter=True,
                callback=self.parse,
                meta={'url': response.meta.get('url')}
            )
        elif '滑动验证页面' in response.text:
            self.logger.warning(f'封禁IP：{response.meta.get("url")}')
        else:
            self.count = 0
            # 职位描述
            jd = ''.join(response.xpath('//div[@class="describe"]//text()').extract())
            # 职位名称
            poname = response.xpath('//span[@class="name"]/span/text()').get()
            # 城市
            city = ''.join(response.xpath('//span[@class="address"]/span//text()').extract())
            # 职位类型
            potype = str(response.xpath('//span[@class="position-type"]//text()').get()).strip()
            # 学历要求
            edu = str(response.xpath('//span[@class="edu-level"]//text()').get()).strip()
            # 招聘人数
            count = str(response.xpath('//span[@class="invite-counts"]/span/text()').get())
            if '人' in count:
                pcount = count.replace('人', '')
            else:
                pcount = count
            # 更新时间
            update_time = response.xpath('//span[@class="time"]/text()').get()
            # 时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 批次
            batch = time.strftime("%Y-%m", time.localtime())

            item = {}
            item['job_url'] = response.url
            item['poname'] = poname
            item['providesalary'] = ''
            item['city'] = city
            item['exp'] = ''
            item['edu'] = edu
            item['pcount'] = pcount
            item['update_time'] = update_time
            item['address'] = ''
            item['welfare'] = ''
            item['skills'] = ''
            item['jd'] = jd
            item['potype'] = potype
            item['created_at'] = created_at
            item['batch'] = batch
            item['recruitment_type'] = '校园招聘'
            item['origin'] = '智联招聘'
            item['status'] = 3
            print(item)


