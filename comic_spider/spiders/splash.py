from bs4 import BeautifulSoup
from ..util import baidu_map
# from scrapy_redis.spiders import RedisSpider
from datetime import datetime
import sys, pickle
import scrapy, requests, re, json, random, time
from pymongo import MongoClient
import scrapy, requests, re, json, random, time
from pymongo import MongoClient
import scrapy
from scrapy_splash import SplashRequest
import os
import logging

logging.basicConfig(level=logging.ERROR,  # 控制台打印的日志级别
                    filename='splash.log',
                    filemode='a',
                    format='%(message)s'
                    )

from comic_spider.peeweedb import *


class SplashSpider(scrapy.Spider):
    name = 'splash'

    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        'SCHEDULER_QUEUE_CLASS': "scrapy_redis.queue.SpiderQueue",
        # 允许暂停，redis请求记录不丢失
        "SCHEDULER_PERSIST": True,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'COOKIE_DEBUG': True,
        'COOKIE_ENABLE': True,
        'SPLASH_COOKIES_DEBUG': True,
        'RETRY_TIMES': 15,
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'REDIS_HOST': "127.0.0.1",
        'REDIS_PORT': 6379,
        'MONGO_URI': 'localhost:27017',
        'MONGO_DATABASE': 'comic',

    }

    def start_requests(self):
        num = 0
        for i in Mobile.select().where(Mobile.id > 8000):
            num += 1
            print(i.id)
            sessionid = i.sessionid
            # sessionid="1dbbtdizf7bqoyrdfm1acdv5za2wcmgc"
            print(sessionid)
            mobile = i.mobile
            print(mobile)
            # splash: init_cookies(splash.args.cookies)
            # "splash:add_cookie{"sessionid","1dbbtdizf7bqoyrdfm1acdv5za2wcmgc","/", domain=".iqing.com"}"
            script1 = "\
                         function main(splash) \
                         splash:add_cookie{'sessionid','"

            script2 = "','/', domain='.iqing.com'}\
                                     assert(splash:go{\
                                     splash.args.url,\
                                     headers=splash.args.headers,\
                                     http_method=splash.args.http_method,\
                                     body=splash.args.body,\
                                     })\
                                     assert(splash:wait(1))\
                                      local entries = splash:history()\
                                   local last_response = entries[#entries].response\
                                     return {\
                                     url = splash:url(),\
                                     http_status = last_response.status,\
                                     cookies=splash:get_cookies(),\
                                     html = splash:html(),\
                                     }\
                           end\
                           "
            script = script1 + sessionid + script2
            cj_url = "https://poi.iqing.com/anniversary/scratch_prize/"
            all_cookies = "_ga=GA1.2.1285990176.1539065896; mobile=1; UM_distinctid=1667704deb2258-0dc55e3d313035-182e1503-1fa400-1667704deb3104e; acw_tc=2463e51b15398589165568587e154ead760f46a32f24daf4a6ab8cf72f; _gid=GA1.2.941759467.1540447123; Hm_lvt_800b4bbdc422aafc13234c4a15581d74=1540532604,1540545570,1540552614,1540558832; bind_mobile=1; _gat=1; username=%E7%94%A8%E6%88%B7_67d391e6; steins_csrf_token=WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT; sessionid={}; avatar=; online=1; id=661333; Hm_lpvt_800b4bbdc422aafc13234c4a15581d74=1540563355".format(
                sessionid)
            all_header = {
                "cookie": all_cookies,
                "origin": "https://www.iqing.com",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
                "x-csrftoken": "WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT",
                "accept": "*/*",
                "referer": "https://www.iqing.com/actopic/80",
                "authority": "poi.iqing.com",
                "x-requested-with": "XMLHttpRequest",
                "content-length": "0",

            }
            splash_args = {
                'wait': 1,
                "url": cj_url,
                "http_method": "POST",
                "headers": all_header,
                "lua_source": script,
                # "cookies":cookies
            }

            yield SplashRequest(
                args=splash_args,
                callback=self.parse,
                meta={"mobile": mobile})
            yield SplashRequest(
                args=splash_args,
                callback=self.parse,
                meta={"mobile": mobile})
            if num >= 300:
                break

        # yield SplashRequest(url, self.parse_next, args={'lua_source': script,
        #                                                 'url': cj_url,
        #                                                 "http_method": "POST",
        #                                                 "body": t2c_data,
        #                                                 "headers": all_header,
        #                                                 }, endpoint='execute')

        # for i in Mobile.select().where(Mobile.id > 6441):
        #     # try:
        #     # time.sleep(5)
        #     # logging.info(i.id)
        #     print(i.id)
        #     print(i.mobile)
        #     # try:
        #     mobile = i.mobile
        #     password = "wearetvxq5"
        #     token = login(mobile, password)
        #     # t2c
        #     t2c_url = "https://poi.iqing.com/user/token_to_cookie/"
        #     t2c_header = {
        #         "origin": "https://m.iqing.com",
        #         "accept-encoding": "gzip, deflate, br",
        #         "accept-language": "zh-CN,zh;q=0.9",
        #         "user-agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        #         "content-type": "application/x-www-form-urlencoded",
        #         "accept": "application/json, text/plain, */*",
        #         "referer": "https://m.iqing.com/login",
        #         "authority": "account.iqing.com",
        #         "cookie": "_ga=GA1.2.1285990176.1539065896; mobile=1; UM_distinctid=1667704deb2258-0dc55e3d313035-182e1503-1fa400-1667704deb3104e; Hm_lvt_ba7c84ce230944c13900faeba642b2b4=1538967114,1539152450,1539761167,1539858919; _gid=GA1.2.941759467.1540447123; Hm_lvt_800b4bbdc422aafc13234c4a15581d74=1540532604,1540545570,1540552614,1540558832; username=%E6%B5%8B%E8%AF%95%E5%93%A5; steins_csrf_token=f1GL6MDFoPLIDwtI69wNAWyNGt9KcedG; id=492688; bind_mobile=1; avatar=http%253A%252F%252Fimage.iqing.in%252Favatar%252F492688%252Fe65503e8-5d02-4e11-98c6-bb00745c3dd9.jpg; _gat=1; online=0; sessionid=pjuxjabwiaud7g8unun46ztr6dgrs2hj; Hm_lpvt_800b4bbdc422aafc13234c4a15581d74=1540559521"
        #     }
        #     t2c_data = {"type": 2,
        #                 "token": token}
        #     t2c_data=json.dumps(t2c_data)

        # 'http_method' is set to 'POST' for POST requests
        # 'body' is set to request body for POST requests

        # script = """
        #      function main(splash)
        #          splash:init_cookies(splash.args.cookies)
        #          assert(splash:go(splash.args.url))
        #          splash:set_viewport_full()
        #
        #          # local search_input = splash:select('input[name=username]')
        #          # search_input:send_text("MY_USERNAME")
        #
        #          # splash:evaljs("document.getElementById('password').value = 'MY_PASSWORD';")
        #
        #          # local submit_button = splash:select('input[name=signin]')
        #          # submit_button:click()
        #
        #          # local entries = splash:history()
        #          # local last_response = entries[#entries].response
        #
        #          return {
        #              cookies = splash:get_cookies(),
        #              headers = last_response.headers,
        #              html = splash:html()
        #                     url = splash:url(),
        #              http_status = last_response.status,
        #          }
        #        end
        #  """
        # splash_args = {
        #     'wait': 1,
        #     "url": t2c_url,
        #     "http_method": "POST",
        #     "body": t2c_data,
        #     "headers": t2c_header,
        #     "lua_source": script,
        # }
        # splash_args = {
        #     'wait': 1,
        #     "url": "https://www.baidu.com",
        #     "http_method": "GET",
        #     # "body": t2c_data,
        #     "headers": t2c_header,
        # }

        # yield SplashRequest(
        #     args=splash_args,
        #     callback = self.parse)
        # break

    def parse(self, response):
        print(response.text)
        mobile = response.meta.get("mobile")
        import re
        msg = re.search(r'({.*})', response.text)
        logging.error(msg)
        logging.error(mobile)
        print(msg)
        dicts = msg[0]
        print(dicts)
        msg2 = json.loads(dicts)
        try:
            id2 = msg2["prize"]["id"]
        except Exception as e:
            print(e)
            return

        #     logging.info(f_result)
        #     if id2 >= 6:
        if id2 >= 6:
            Jiangpin.create(
                jiangpin=id2,
                mobile=mobile,
                time=datetime.now()
            )
        #         logging.info("恭喜中奖" + str(f_result))
        #         print("恭喜中奖" + str(f_result) + str(mobile))

        # cj_url = "https://poi.iqing.com/anniversary/scratch_prize/"
        # all_cookies = "_ga=GA1.2.1285990176.1539065896; mobile=1; UM_distinctid=1667704deb2258-0dc55e3d313035-182e1503-1fa400-1667704deb3104e; acw_tc=2463e51b15398589165568587e154ead760f46a32f24daf4a6ab8cf72f; _gid=GA1.2.941759467.1540447123; Hm_lvt_800b4bbdc422aafc13234c4a15581d74=1540532604,1540545570,1540552614,1540558832; bind_mobile=1; _gat=1; username=%E7%94%A8%E6%88%B7_67d391e6; steins_csrf_token=WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT; sessionid=; avatar=; online=1; id=661333; Hm_lpvt_800b4bbdc422aafc13234c4a15581d74=1540563355"
        # all_header = {
        #     "cookie": all_cookies,
        #     "origin": "https://www.iqing.com",
        #     "accept-encoding": "gzip, deflate, br",
        #     "accept-language": "zh-CN,zh;q=0.9",
        #     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
        #     "x-csrftoken": "WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT",
        #     "accept": "*/*",
        #     "referer": "https://www.iqing.com/actopic/80",
        #     "authority": "poi.iqing.com",
        #     "x-requested-with": "XMLHttpRequest",
        #     "content-length": "0",
        # }
        # t2c_data = ""
        # yield SplashRequest(url=cj_url,
        #                     http_method="POST",
        #                     body=t2c_data,
        #                     headers=all_header,
        #                     cookies=cookie,
        #                     endpoint='execute',
        #                     callback=self.jp_parse)

    def parse2(self, response):
        # cookie = response.data["cookies"]
        # scratch_chances = shoucang(cookie)

        # cookiejar = response.data["cookies"]
        # for i in range(0, len(scratch_chances)):
        script = """
                       function main(splash)
                        splash:add_cookie{'sessionid',
                         """

        script2 = """
                         , "/", domain=".iqing.com"}
                        assert(splash:go{
                        splash.args.url,
                        headers=splash.args.headers,
                        http_method=splash.args.http_method,
                        body=splash.args.body,
                        })
                        assert(splash:wait(0.5))
                        local entries = splash:history()
                        return {
                        url = splash:url(),
                        headers = last_response.headers,
                        http_status = last_response.status,
                        cookies=splash:get_cookies(),
                        html = splash:html(),
                        }

                      end
               """
        str = script.format("123")
        cj_url = "https://poi.iqing.com/anniversary/scratch_prize/"
        all_cookies = "_ga=GA1.2.1285990176.1539065896; mobile=1; UM_distinctid=1667704deb2258-0dc55e3d313035-182e1503-1fa400-1667704deb3104e; acw_tc=2463e51b15398589165568587e154ead760f46a32f24daf4a6ab8cf72f; _gid=GA1.2.941759467.1540447123; Hm_lvt_800b4bbdc422aafc13234c4a15581d74=1540532604,1540545570,1540552614,1540558832; bind_mobile=1; _gat=1; username=%E7%94%A8%E6%88%B7_67d391e6; steins_csrf_token=WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT; sessionid=; avatar=; online=1; id=661333; Hm_lpvt_800b4bbdc422aafc13234c4a15581d74=1540563355"
        all_header = {
            "cookie": all_cookies,
            "origin": "https://www.iqing.com",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
            "x-csrftoken": "WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT",
            "accept": "*/*",
            "referer": "https://www.iqing.com/actopic/80",
            "authority": "poi.iqing.com",
            "x-requested-with": "XMLHttpRequest",
            "content-length": "0",

        }
        t2c_data = ""
        yield SplashRequest(url, self.parse_next, args={'lua_source': script,
                                                        'url': cj_url,
                                                        "http_method": "POST",
                                                        "body": t2c_data,
                                                        "headers": all_header,
                                                        }, endpoint='execute')

    def jp_parse(self, response):
        print(response.status_code)
        print(requests.text)
        if response.status_code != 200:
            print(response.text)
            f_result = {"prize": {"id": -1}}
            return cookies, f_result, sessionid
        f_result = response.json()
        if str(f_result["code"]) == "-2":
            f_result = {"prize": {"id": -1}}
        logging.info(f_result)
        return f_result
