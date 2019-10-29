# -*- coding: utf-8 -*-
import codecs
import hashlib
import re
from urllib import parse

import scrapy

from ..items import MyscrapyJianshuItem


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = []
    # start_urls = ['http://jianshu.com/']
    # start_urls = ['https://www.jianshu.com/p/33b1c5d0fbca']
    # 只修改下面网址就可运行
    start_urls = ['https://www.jianshu.com/p/28fb20245e05']
    print('程序开始运行......')

    def parse(self, response):
        print('开始运行parse')
        try:
            content = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]').extract_first()
            item = MyscrapyJianshuItem()
            item['image_urls'] = []
            site = 'https://www.jianshu.com/'
            image_urls = response.xpath('//img/@data-original-src').extract()
            for image_url in image_urls:
                full_image_url = parse.urljoin(site, image_url)
                item['image_urls'].append(full_image_url)
                # 用哈希码替换正文中图片的url，因为默认下载的图片文件名是哈希码
                image_name = 'images/' + self.sha1(full_image_url) + '.jpg'
                print(image_name)
                content = content.replace(image_url, image_name)
            yield item
            # 去掉html中的这些，否则图片显示位置不正确
            pattern = '<div class="image-container-fill" style="padding-bottom: \d+\.\d+%;"></div>'
            content = re.sub(pattern=pattern, repl='', string=content)
            # 去掉这些，否则图片不显示
            pattern = 'data-original-'
            content = re.sub(pattern=pattern, repl='', string=content)
            # 输出重构的文件
            filename = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/h1/text()').extract_first()
            filename = 'outputs/' + filename + '.html'
            with codecs.open(filename, 'w', 'utf-8') as f:
                f.write(content)
        except Exception as e:
            print('parse出错', e)
        pass

    @staticmethod
    def sha1(name):
        """ 将图片url转成哈希码 """
        if not isinstance(name, str):
            name = str(name)
        sha1 = hashlib.sha1()
        sha1.update(name.encode('utf-8'))
        return sha1.hexdigest()
