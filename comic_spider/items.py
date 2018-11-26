# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文件名, 章节名
    dir_name = scrapy.Field()
    # 每个章节每一页的链接
    link_url = scrapy.Field()
    # 图片链接
    img_url = scrapy.Field()
    # 图片保存路径
    # image_path = scrapy.Field()


class GalleryItem(scrapy.Item):
    title = scrapy.Field()
    domain = scrapy.Field()
    insert_time = scrapy.Field()
    gallery_id = scrapy.Field()
    all_page = scrapy.Field()
    tags = scrapy.Field()
    publish_time = scrapy.Field()
    from_id = scrapy.Field()


class ImageItem(scrapy.Item):
    image_url = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    order = scrapy.Field()
    gallery_id = scrapy.Field()


