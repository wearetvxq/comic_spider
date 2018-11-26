import requests,json,random
import requests,time
from bs4 import BeautifulSoup
from pymongo import MongoClient
import redis
try:
    red = redis.StrictRedis(host='127.0.0.1', port=6379)
except Exception as e:
    print (e.message)

def baidu_map(address):
    if address != '0':
        url1 = 'https://api.map.baidu.com/geocoder/v2/?address=' + address + '&output=json&ak=gRManfxm4xGfswhaIT4xGh78UpHV8kCV'
        r = requests.get(url1)
        r.status_code
        result = json.loads(r.text)
        x = result['result']['location']['lng']
        y = result['result']['location']['lat']
        url2 = 'https://api.map.baidu.com/geocoder/v2/?location=' + str(y) + ',' + str(
            x) + '&output=json&pois=0&ak=gRManfxm4xGfswhaIT4xGh78UpHV8kCV'
        r1 = requests.get(url2)
        result1 = json.loads(r1.text)
        prov = result1['result']['addressComponent']['province']
        city = result1['result']['addressComponent']['city']
        area = result1['result']['addressComponent']['district']
        return (prov, city)

#有时间用flask做代理池
#scrapy 就不用了  {'proxy': 'http://proxy.yourproxy:8001';})
def get_proxy():
    count = red.llen("proxies:proxy")
    proxies = red.lrange("proxies:proxy", 0, count - 1)
    red.ltrim("proxies", count, -1)

    rint = random.randint(1,count)
    ip=proxies[int(rint)-1]
    ip = str(ip, encoding="utf8")
    proxies = {
        'https': ip
    }

    urlmid = 'https://m.qixin.com'
    try:
        r = requests.get(urlmid, proxies=proxies, timeout=3)
        if r.status_code == 200:
            return ip
    except:
        pass

