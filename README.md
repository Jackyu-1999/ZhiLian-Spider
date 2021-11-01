# Scrapy+Pyecharts实现智联招聘爬虫和数据可视化

## 快速上手

- 在安装好git的情况下可以使用如下命令：

```
git clone https://github.com/Jackyu-1999/ZhiLian-Spider.git
```

或者直接下载zip压缩包到本地。

- 建议使用Pycharm直接运行main.py，根据提示输入学历类型ID，例如：4（代表本科）
- 当然还可以利用以下参数拼接url：
  -   pageSize: 返回数据的数量，默认返回50条，最多返回90条

  -   pageNo: 翻页参数，默认为1

  -   cityId: 城市id，默认为-1，如：`长沙`的id为 `749`

  -   workExperience: 工作经验参数，默认为-1，如：`1-3年` 经验为 `0103`

  -   jobType: 职位类型id，默认为-1，如：`javascript前端工程师为` `9000100030000（小类）`

  -   education: 学历要求，默认为-1，如：`本科` 为 `4`

  -   companyType: 公司性质，默认为-1，如：`国企` 为 `1`

  -   companySize: 公司规模，默认为-1，如：`100-299人` 为 `3`

## 开发环境

本项目所使用的开发环境版本如下：

- python 3.6.12
- pyecharts 1.9.0
- pymongo 3.10.1
- scrapy 2.0.1
- numpy 1.19.4


## 2021.11.1号经测试仍然可用

<img align="center" alt="GIF" width="400px" src="https://cdn.jsdelivr.net/gh/Jackyu-1999/CDN-Static@main/star.png" />

***



   
