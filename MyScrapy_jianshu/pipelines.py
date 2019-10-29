# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class MyscrapyJianshuPipeline(object):
    def process_item(self, item, spider):
        return item


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
