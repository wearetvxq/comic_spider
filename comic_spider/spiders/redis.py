# -*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# #from scrapy.spiders import CrawlSpider, Rule
# from scrapy.spiders import Rule
# from scrapy_redis.spiders import RedisCrawlSpider
# from youyuan.items import YouyuanItem
# import re
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
import scrapy
import sys
import scrapy,requests,re,urllib,json,random,time
from pymongo import MongoClient
import logging as log
from youyuan.items import *

import io

from youyuan.common.rule_manager import RuleManager

rule={
    "domain": "www.meizitu.com",
    "list": {
        "list_url": "http://www.meizitu.com/a/{listid}_{page}.html",
        "all_page": {
            "xpath": "//div[@id='wp_page_numbers']/ul/li[last()]/a/@href",
            "regex": ".*?(\d+).*"
        },
        "gallery_block": "//li[@class='wp-item']",
        "gallery_id": {
            "xpath": ".//h3[@class='tit']/a/@href",
            "regex": ".*?(\d+).*"
        },
    },
    "gallery": {
        "gallery_url": "http://www.meizitu.com/a/{galleryid}.html",
        "image_block": "//div[@id='picture']//img",
        "image_url": "./@src",
        "title": "//div[@class='metaRight']/h2/a/text()",
        "desc": "./@alt",
        "need_flip": False,
        "tags": "//div[@class='metaRight']/p/text()"
    }
}
seed=[
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___cute", "extends": {"tags": ["可爱", "萌妹"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___xinggan", "extends": {"tags": ["性感"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___sifang", "extends": {"tags": ["私房"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___qingchun", "extends": {"tags": ["清纯"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___meizi", "extends": {"tags": ["清纯"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___xiaoqingxin", "extends": {"tags": ["小清新", "清纯"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___nvshen", "extends": {"tags": ["女神"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___qizhi", "extends": {"tags": ["气质"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___moto", "extends": {"tags": ["模特"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___bijini", "extends": {"tags": ["比基尼", "性感"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___baobei", "extends": {"tags": ["足球", "体育"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___luoli", "extends": {"tags": ["萝莉", "可爱"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___wangluo", "extends": {"tags": ["网络"]}},
{"domain": "www.meizitu.com", "_id": "www.meizitu.com___rihan", "extends": {"tags": ["日韩", "国外"]}},
]

#失败的美女图片爬虫
class YySpider(RedisSpider):
    name = 'yy'
    redis_key = "beauty"
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}

    def make_request_from_data(self, data): #data就是域名了
        for i in seed:
            if i["domain"]==data:
                page=1
                _id = i.get("_id")

                meta = {"_id": _id,
                        "domain": data,
                        "extends": i["extends"],
                        "page": page,
                        "url":""
                        }
                self.page_parse(meta)


        # meta=data
        # meta['task']=data
        # url=data["domain"]
        # page=1
        # _id = data.get("_id")
        # domain, _id = _id.split("___")
        # rule.get("domain", "")
        # if page == 1:
        #     url = rule.get("list_first_url", rule.get("list_url", "")).format(listid=_id, page=page)
        # else:
        #     url = rule.get("list_url").format(listid=_id, page=page)
        # return url
        # self.gen_request_from_url(url,meta)

    def page_parse(self,meta):
        _id=meta['_id']
        page=meta['page']
        domain, _id = _id.split("___")
        list_first_url = rule['list']['list_url'].format(_id, page)
        url=list_first_url
        yield Request(url,callback=self.parse_list(),meta=meta)



    def parse_list(self, response):
        meta=response.meta
        _id=response.meta.get("_id")
        domain =response.meta.get("domain")
        extends = response.meta.get("extends")
        from youyuan.common.parser import ListParser
        ListParser=ListParser(rule=rule['list'])
        # list页面解析，获取直接能获取的字段
        list_items, all_page = ListParser(response)
        # 字段加工，增加额外的字段
        for item in list_items:
            item['insert_time'] = int(time.time())
            item['from_id'] = _id
            item['domain'] = domain
            # 继承seed中extend里的元素
            self.__append_extend(item, extends)
            item['order'] = 1
            item['gallery_id'] = item['from_id'] + "___" + item['_id']
            url = self.rule_manager.gen_detail_url(item, page=1)
            yield Request(url, meta={"gallery": item}, callback=self.parse_gallery, dont_filter=True)
        now_page = meta.get("page")
        # 需要一个中间层来包page
        if now_page < all_page:
            meta['page'] = now_page + 1
            yield self.page_parse(meta)

    def parse_gallery(self, response):
        gallery = response.meta.copy().get("gallery")
        now_page = gallery.get("order")

        GalleryParser
        image_items = self.rule_manager.parse_detail(gallery, response)
        for index, item in enumerate(image_items):
            item["gallery_id"] = gallery.get("gallery_id")
            item['order'] = self.rule_manager.order_calculate(gallery, now_page, index)
            yield self.__gen_image_item(item)
        if len(image_items) >= 1:
            first_image = image_items[0]
            # 第一页需要抛出gallery
            if now_page == 1:
                yield self.__gen_gallery_item(gallery, first_image)
            # 是否需要翻页
            if self.rule_manager.need_flip(gallery):
                all_page = int(first_image.get("all_page"))
                if now_page < all_page:
                    url = self.rule_manager.gen_detail_url(gallery, page=now_page + 1)
                    gallery['order'] = now_page + 1
                    yield Request(url, meta={"gallery": gallery}, callback=self.parse_gallery, dont_filter=True)
                else:
                    print("get all image for gallery {gallery}".format(gallery=gallery.get("gallery_id")))

    def __gen_gallery_item(self, gallery_item, first_image):
        gallery = GalleryItem()
        for k in gallery.fields.keys():
            if k in gallery_item and gallery_item[k] is not None:
                gallery[k] = gallery_item[k]
            elif k in first_image and first_image[k] is not None:
                gallery[k] = first_image[k]
        # 特殊处理tags
        if "tags" in first_image and first_image['tags'] is not None:
            tags = list(set(gallery_item.get("tags", []) + first_image.get("tags", [])))
            gallery['tags'] = tags
        return gallery

    def __gen_image_item(self, item):
        image = ImageItem()
        for k in image.fields.keys():
            if k in item and item[k] is not None:
                image[k] = item[k]
        return image

    def __append_extend(self, _to, _from):
        for k, v in _from.iteritems():
            if isinstance(v, basestring):
                if k not in _to:
                    _to[k] = v
            if isinstance(v, list):
                _to[k] = _to.get(k, []) + v
        return _to
