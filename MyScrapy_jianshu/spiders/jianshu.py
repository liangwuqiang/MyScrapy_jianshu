# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from ..items import MyscrapyJianshuItem


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = []
    start_urls = [
        # 'https://www.jianshu.com/p/33b1c5d0fbca',  # 清华北大学霸学习方法（思维导图总结）
        'https://www.jianshu.com/p/6bc5a4641629',  # 爬虫框架Scrapy的安装与基本使用
        # 'https://www.jianshu.com/p/28fb20245e05',  # Python正则表达式
        # 'https://www.jianshu.com/p/a167aa9cb61c',  # 实战：爬取简书之多线程爬取（一）
    ]
    print('程序开始运行......')

    def parse(self, response):
        print('开始运行parse')
        try:
            url = response.url
            title = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/h1/text()').extract_first()
            content = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]').extract_first()
            image_srcs = response.xpath('//img/@data-original-src').extract()

            item = MyscrapyJianshuItem()
            item['url'] = url
            item['title'] = title
            item['content'] = content
            item['image_srcs'] = image_srcs  # 不完整路径，用于查找替换图片链接
            item['image_urls'] = []  # 完整路径
            for image_src in image_srcs:
                site = 'https://www.jianshu.com/'
                image_url = parse.urljoin(site, image_src)
                item['image_urls'].append(image_url)

            yield item
            print(title)
        except Exception as e:
            print('parse出错', e)
        pass


