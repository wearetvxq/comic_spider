# - * - coding: utf-8 - * -
from scrapy import Spider
import scrapy
import requests
import itertools
import json, time
import urllib.parse

from json import *
from bs4 import BeautifulSoup
from pymongo import MongoClient
import jieba.posseg as pseg
import urllib.request
from time import sleep
import re, os


class PhoneSpider(scrapy.Spider):
    name = "phone"

    def mongo(self):
        conn = MongoClient('127.0.0.1', 27017)
        return conn

    def __init__(self):
        self.headers = {
            'Content-Type': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

        self.cookies = {'BD_CK_SAM': '1', 'BDSVRTM': '126',
                        'H_PS_645EC': 'ef78iIXTHUvw1iD5bSdOvGIpOHYYNIZy4GxzVWYjkK%2FfRJ8DikBG%2F2ZFTV0',
                        'PSTM': '1525179832', 'H_PS_PSSID': '1454_21082_26350_20719',
                        'BAIDUID': '3987F0F0FA5CA994ED2A9B12E7505A04:FG',
                        'BIDUPSID': '3987F0F0FA5CA994ED2A9B12E7505A04', 'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
                        'BD_HOME': '0', 'PSINO': '1', 'MCITY': '-218%3A', 'BD_UPN': '123353'}

    def start_requests(self):
        conn = self.mongo()
        db = conn.phonenumber

        i = 0
        k=377386  #28
        # k=100302
        # k= 253896
        # k= 150302
        # k= 200302
        # k=300000
        # k = 350000
        # k = 400000
        cursor = db.GLphone.find({}, no_cursor_timeout=True).skip(k)
        for item in cursor:
            # for item in db.GLphone.find({}).skip(253695):

            i = i + 1
            print(i + k)
            if i >= 1:
                url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=' + str(
                    item['CALLEDNUM'])  # CALLEDNUM
                yield scrapy.Request(
                    url=url,
                    cookies=self.cookies,

                    headers=self.headers,
                    meta={'phone': item['CALLINGNUM']},
                    callback=self.parse,
                    dont_filter=True
                )
        cursor.close()

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        info = {}
        info['phone'] = response.meta['phone']
        info['prov'] = '0'
        info['city'] = '0'
        info['type'] = '0'
        info['is_lj'] = '0'
        info['lj_type'] = '0'

        info['baidu'] = '0'
        info['baidu_num'] = '0'
        info['baidu_name'] = '0'  # 骚扰
        info['360'] = '0'
        info['360_num'] = '0'
        info['360_name'] = '0'
        info['sogou'] = '0'
        info['sogou_num'] = '0'
        info['sogou_name'] = '0'

        try:
            if soup.find(class_="c-border op_fraudphone_container") != None:
                if soup.find(class_="op_fraudphone_label_tx") == None:
                    type = soup.find(class_="op_fraudphone_word").find("strong").text.replace('"', '')
                    info['baidu_name'] = type
                else:
                    type = soup.find(class_="op_fraudphone_label_tx").text  # 垃圾电话类型
                    info['baidu_name'] = type
                    info['baidu'] = '1'

                num = soup.find(class_="op_fraudphone_word").text.split('百度手机卫士')[0].replace('被', '').replace('个',
                                                                                                              '').replace(
                    "\n", "").strip()  # 被标记次数
                num = re.sub("\D", "", num)
                info['baidu_num'] = num
        except:
            pass
        yield scrapy.Request(
            url='https://www.so.com/s?q=' + info['phone'],
            meta=info,
            callback=self.parse_360,
            dont_filter=True,
        )

    def parse_360(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        info = response.meta

        try:
            if soup.find(class_="mohe-ph-mark") != None:
                try:
                    type = soup.find(class_="mohe-ph-mark").text.strip()  # 垃圾电话类型
                    info['360'] = '1'
                    info['360_name'] = type
                except:
                    pass

                try:
                    user_image = soup.find("strong", attrs={"class": "mohe-tips mh-hy"}).find("img").get('src')
                    info['360_name'] = user_image
                except:
                    user_image = '0'
                try:
                    num = soup.find(class_="mohe-tips").find_all('span')[1].find('b').text  # 被标记次数
                except:
                    num = soup.find_all(class_="mohe-tips")[2].find_all('span')[1].find('b').text
                info['360_num'] = num
        except:
            pass

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.sogou.com',
            'Referer': 'https://m.sogou.com/?prs=9&rfh=1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        }

        cookies = {'FREQUENCY': '1525252267102_5', 'usid': 'y28FmBb-6I-ws5GU', 'userGroupId': '3',
                   'ABTEST': '0|1525252229|v1', 'SNUID': 'EE6CF1315E5B36682B06017E5E8EBC09',
                   'ld': 'ryllllllll2zfYjVlllllVrr7WklllllbfDe7lllllwlllllxllll5@@@@@@@@@@',
                   'SUID': 'B031AF6F5118910A000000005AE98093', 'IPLOC': 'CN4201', 'wuid': 'AAEV1kzfHwAAAAqRIi3HYQcAAAA',
                   'SUV': '000930416FAF31B05AE98085A9022911'}

        yield scrapy.Request(
            url='https://m.sogou.com/web/searchList.jsp?keyword=' + info['phone'],
            meta=info,
            callback=self.parse_sogou,
            dont_filter=True,
            cookies=cookies,
            headers=headers
        )

    def parse_sogou(self, response):

        info = response.meta

        try:
            soup = BeautifulSoup(response.body.decode('UTF-8'), "lxml")
            if (soup.find(id='sogou_vr_10001001_1') != None):
                datas = soup.find(class_="text-layout").find('p').find('span').text.split(' ')
                if not datas[0]:
                    type = datas[1]
                    info['sogo_name'] = datas[1]
                else:
                    type = datas[0]
                    info['sogou'] = '1'
                    info['sogo_name'] = datas[0]
        except:
            pass

        phone = info['phone']
        try:
            url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={}&co=&resource_id=6004&t=1525240171994&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery11020957531216439552_1525239975389&_=1525239975408'.format(
                phone)
            r = requests.get(url)

            print(r.text)
            data = r.text.replace('/**/jQuery11020957531216439552_1525239975389(', '').replace(');', '')
            data = json.loads(data)
            info['prov'] = data["data"][0]['prov']
            info['city'] = data["data"][0]['city']
            info['type'] = data["data"][0]['type']
        except:
            pass
        if (info['360'] == '1') or (info['baidu'] == '1') or (info['sogou'] == '1'):
            print(info)
            yield info
