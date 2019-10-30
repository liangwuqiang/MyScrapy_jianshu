# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import codecs
import hashlib
import re
from urllib import parse


class MyscrapyJianshuPipeline(object):
    def process_item(self, item, spider):
        url = item['url']
        title = item['title']

        content = item['content']
        for image_src in item['image_srcs']:
            site = 'https://www.jianshu.com/'
            image_url = parse.urljoin(site, image_src)
            # 用哈希码替换正文中图片的url，因为默认下载的图片文件名是哈希码
            image_name = 'images/' + self.sha1(image_url) + '.jpg'
            content = content.replace(image_src, image_name)
        # 否则图片显示位置不正确
        pattern = '<div class="image-container-fill" style="padding-bottom: \d+\.\d+%;"></div>'
        content = re.sub(pattern=pattern, repl='', string=content)
        # 否则图片不显示
        pattern = 'data-original-'
        content = re.sub(pattern=pattern, repl='', string=content)

        filename = 'outputs/' + title + '.html'
        with codecs.open(filename, 'w', 'utf-8') as f:
            f.write(self.html_format(url, title, content))
        return item

    @staticmethod
    def sha1(name):
        """ 将图片url转成哈希码 """
        if not isinstance(name, str):
            name = str(name)
        sha1 = hashlib.sha1()
        sha1.update(name.encode('utf-8'))
        return sha1.hexdigest()

    @staticmethod
    def html_format(url, title, content):
        html_template = """<!DOCTYPE html>
        <html><head><meta charset="UTF-8">
        </head><body>
        <p><a href="{url}">原文链接</a></p>
            {content}
        </body></html>"""
        html = html_template.format(url=url, title=title, content=content)
        return html


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        path = super(MyImagesPipeline, self).file_path(request, response, info)
        image_name = path.replace("full/", "")  # 去掉默认的full目录
        return image_name

    def get_media_requests(self, item, info):
        try:
            for image_url in item['image_urls']:
                print('图片下载>> ', image_url)
                yield scrapy.Request(image_url)
        except Exception as e:
            print('get_media_requests出错', e)
    pass
