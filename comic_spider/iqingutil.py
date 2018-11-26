
def get_sms_code(mobile):
    token = "0095856209dfb756353d54f9d42b89c19da03f578d01"
    id = "894"
    sms_code_url3 = "http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token={}&itemid={}&mobile={}&release=1".format(
        token, id, mobile)
    sms_code = ""
    times = 0
    while (not sms_code) and (times <= 5):
        sms_code_r3 = requests.get(sms_code_url3)
        print(sms_code_r3.text)
        if sms_code_r3.text == "3001":
            time.sleep(3)
            times += 1
        else:
            print(sms_code_r3.text)
            import re
            sms_code = re.search(r'(\d+)', sms_code_r3.text)[0]
            print(sms_code)
    if sms_code:
        return sms_code
    else:
        return False


def reg(mobile, sms_code):
    reg_url = "https://api.iqing.in/v3/register/"

    reg_header = {
        "Accept-Encoding": "gzip",
        "Ali-Cdn-Real-Ip": "223.104.106.158",
        "Ali-Swift-Log-Host": "api.iqing.in",
        "Ali-Swift-Skip": "on",
        "Ali-Swift-Stat-Host": "api.iqing.in",
        "Ali-Tproxy-Origin-Host": "api.iqing.in",
        "Appversion": "v3",
        "Build": "24",
        "Connection": "close",
        "Content-Type": "application/json; charset=utf-8",
        "Eagleeye-Traceid": "78c0528915405557096457989e",
        "Guid": "a1904df7",
        "Host": "api.iqing.in",
        "Remoteip": "106.15.218.29",
        "System": "android",
        "User-Agent": "iqing-android",
        "Version": "SM-G9006V,23,6.0.1",
        "Via": "cn104.l1, l2et15-2.l2",
        "X-Client-Scheme": "https",
        "X-Forwarded-For": "223.104.106.158, 106.15.218.29, 100.116.200.7, 172.22.212.3",
        "X-Forwarded-Proto": "https",
        "X-Real-Ip": "172.22.212.3",
    }
    password = "wearetvxq5"

    reg_data = {"code": sms_code,
                "mobile": mobile,
                "password": password,
                "quick": 1}
    import json
    reg_data = json.dumps(reg_data)
    # {"mobile":"18843501641",
    # "code":543036,
    # "password":"wearetvxq5",
    # 	"quick":1
    # }
    reg_r = requests.post(url=reg_url, data=reg_data, headers=reg_header)
    # print(reg_r.text)
    print(reg_r.status_code)
    # logging.info(reg_r.status_code)

    reg_result = reg_r.json()
    print(reg_result)
    token = reg_result["token"]
    print(token)
    logging.info(token)
    return token


def login(mobile, password):
    log_url = "https://api.iqing.in/v3/login/"
    log_header = {
        "Accept-Encoding": "gzip",
        "Appversion": "v3",
        "Build": "32802",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Country": "5Lit5Zu9",
        "Guid": "a73da857",
        "Host": "api.iqing.in",
        "Remoteip": "58.48.77.128",
        "System": "android",
        "User-Agent": "iqing-android",
        "Version": "Mi-4c,24,7.0",
        "X-Forwarded-For": "58.48.77.128, 100.116.221.112, 172.20.21.38",
        "X-Forwarded-Proto": "https",
        "X-Real-Ip": "172.20.21.38",
    }
    # 不用login
    log_data = {"password": password,
                "mobile": mobile}

    try:
        log_r = requests.post(url=log_url, data=log_data, headers=log_header)
        if log_r.status_code == 200:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            log_result = log_r.json()
            token = log_result["token"]
            print(token)
            return token
    except requests.exceptions.Timeout:
        NETWORK_STATUS = False  # 请求超时改变状态
        if NETWORK_STATUS == False:
            for i in range(1, 10):
                log_r = requests.post(url=log_url, data=log_data, headers=log_header)
                if log_r.status_code == 200:
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    log_result = log_r.json()
                    token = log_result["token"]
                    print(token)
                    return token
                    NETWORK_STATUS = True
                    break
    except Exception:
        log_r = requests.post(url=log_url, data=log_data, headers=log_header)
        if log_r.status_code == 200:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            log_result = log_r.json()
            token = log_result["token"]
            print(token)
            return token
    # except requests.exceptions.Timeout:
    #     global NETWORK_STATUS
    #     NETWORK_STATUS = False  # 请求超时改变状态
    #     if NETWORK_STATUS == False:
    #         for i in range(1, 10):
    #             log_r = requests.post(url=log_url, data=log_data, headers=log_header, timeout=8)
    #             if log_r.status_code == 200:
    #                 print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #                 log_result = log_r.json()
    #                 token = log_result["token"]
    #                 print(token)
    #                 return token
    # logging.info(log_r.status_code)
    # logging.info(token)


def t2c(token):
    t2c_url = "https://poi.iqing.com/user/token_to_cookie/"
    t2c_header = {
        "origin": "https://m.iqing.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json, text/plain, */*",
        "referer": "https://m.iqing.com/login",
        "authority": "account.iqing.com",
        "cookie": "_ga=GA1.2.1285990176.1539065896; mobile=1; UM_distinctid=1667704deb2258-0dc55e3d313035-182e1503-1fa400-1667704deb3104e; Hm_lvt_ba7c84ce230944c13900faeba642b2b4=1538967114,1539152450,1539761167,1539858919; _gid=GA1.2.941759467.1540447123; Hm_lvt_800b4bbdc422aafc13234c4a15581d74=1540532604,1540545570,1540552614,1540558832; username=%E6%B5%8B%E8%AF%95%E5%93%A5; steins_csrf_token=f1GL6MDFoPLIDwtI69wNAWyNGt9KcedG; id=492688; bind_mobile=1; avatar=http%253A%252F%252Fimage.iqing.in%252Favatar%252F492688%252Fe65503e8-5d02-4e11-98c6-bb00745c3dd9.jpg; _gat=1; online=0; sessionid=pjuxjabwiaud7g8unun46ztr6dgrs2hj; Hm_lpvt_800b4bbdc422aafc13234c4a15581d74=1540559521"
    }
    t2c_data = {"type": 2,
                "token": token}
    t2c_r = requests.post(url=t2c_url, data=t2c_data, headers=t2c_header)
    print(t2c_r.status_code)
    cookies = t2c_r.cookies
    cookies_dict = str(cookies._cookies)
    print(cookies_dict)
    import re

    sessionid = re.search(r'value=(.*), port=', cookies_dict)[0].replace("value=\'", "").replace("\', port=", "")
    print(sessionid)
    print('~~~~~~~~~~~~~~~~~~~')
    sessionid = sessionid.split("None")[0]

    return cookies, sessionid


def cj(cookies, sessionid):
    print(sessionid)
    print(cookies)
    # cookies=cookies.get_dict()
    # sessionid="sessionid={}; path=/; domain=.iqing.com; HttpOnly; Expires=Tue, 19 Jan 2038 03:14:07 GMT;".format(sessionid)
    cookies = {"sessionid": sessionid,
               "path": "/",
               "domain": ".iqing.com",
               }
    print(cookies)

    # sessionid
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

    cj_r = requests.post(url=cj_url, cookies=cookies, headers=all_header)
    print(cj_r.status_code)
    if cj_r.status_code != 200:
        print(cj_r.text)
        f_result = {"prize": {"id": -1}}
        return cookies, f_result, sessionid
    f_result = cj_r.json()
    if str(f_result["code"]) == "-2":
        f_result = {"prize": {"id": -1}}
    logging.info(f_result)
    return f_result


def cj2(cookies, sessionid):
    cookies_dict = str(cookies._cookies)
    print(cookies_dict)
    cj_url = "https://poi.iqing.com/anniversary/scratch_prize/"
    all_cookies = "_ga=GA1.2.1285990176.1539065896; mobile=1; UM_distinctid=1667704deb2258-0dc55e3d313035-182e1503-1fa400-1667704deb3104e; acw_tc=2463e51b15398589165568587e154ead760f46a32f24daf4a6ab8cf72f; _gid=GA1.2.941759467.1540447123; Hm_lvt_800b4bbdc422aafc13234c4a15581d74=1540532604,1540545570,1540552614,1540558832; bind_mobile=1; _gat=1; username=%E7%94%A8%E6%88%B7_67d391e6; steins_csrf_token=WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT; sessionid={}; avatar=; online=1; id=661333; Hm_lpvt_800b4bbdc422aafc13234c4a15581d74=1540563355".format(
        sessionid)
    cj_header = {
        "origin": "https://www.iqing.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "x-csrftoken": "WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "*/*",
        "cookie": all_cookies,
        "referer": "https://www.iqing.com/actopic/80",
        "authority": "poi.iqing.com",
        "x-requested-with": "XMLHttpRequest",
        "content-length": "0",
    }

    cj_r = requests.post(url=cj_url, headers=cj_header, cookies=cookies)
    print(cj_r.status_code)
    if cj_r.status_code != 200:
        print(cj_r.text)
        f_result = {"prize": {"id": -1}}
        return cookies, f_result, sessionid
    f_result = cj_r.json()
    if str(f_result["code"]) == "-2":
        f_result = {"prize": {"id": -1}}
    logging.info(f_result)
    return f_result


##蚂蚁

def my_login():
    myname = "wearetvxq"
    mypwd = "wearetvxq"
    Developer = "zhIJr2g%2bNIIxAUY3a%2btQNA%3d%3d"
    sh_url = "http://api.shjmpt.com:9002/pubApi/uLogin?uName={}&pWord={}&Developer={}".format(myname, mypwd, Developer)
    # my_url="http://www.66yzm.com/api/admin/dengl?zhanghao={}&mima={}".format(myname,mypwd)
    r = requests.get(sh_url)
    print(r.text)
    # token=r.json()["token"]
    # "1a10d2e40461c42afd0913ed1bcb413f"
    # "s4oJLGYtpwFrb2klJCd8cYCylU0JWxM36M3309729"


def my_get_mobile():
    # linpai="1a10d2e40461c42afd0913ed1bcb413f"
    # id="61"
    # url="http://www.66yzm.com/api/admin/getmobile?linpai={}&itemid={}".format(linpai,id)

    linpai = "d8131doI5UPIdF8zPuvIABFREKNdFxE39E3309729"
    id = "14803"
    url = "http://api.shjmpt.com:9002/pubApi/GetPhone?ItemId={}&token={}".format(id, linpai)
    r = requests.get(url)
    print(r.text)
    mobile = r.text.replace(";", "")
    return mobile


def get_my_sms_code(mobile):
    linpai = "d8131doI5UPIdF8zPuvIABFREKNdFxE39E3309729"
    id = "14803"
    url = "http://api.shjmpt.com:9002/pubApi/GMessage?token={}&ItemId={}&Phone={}".format(linpai, id, mobile)

    sms_code = ""
    times = 0
    while (not sms_code) and (times <= 5):
        r = requests.get(url)
        print(r.text)
        if str(r.text).startswith("MSG"):
            msg = str(r.text).split("&")[-1]
            msg = re.search(r'(\d+)', msg)[0]
            sms_code = msg
            print(sms_code)
        else:
            time.sleep(3)
            times += 1
    if sms_code:
        return sms_code
    else:
        return False


def shoucang(cookie):
    t2c_url = "https://poi.iqing.com/anniversary/scratch_chances/?share=1"
    cj_header = {
        "origin": "https://www.iqing.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "x-csrftoken": "WfNxT1tzmjXFCppYDU75FZ2peQ2m3DTT",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "*/*",
        "referer": "https://www.iqing.com/actopic/80",
        "authority": "poi.iqing.com",
        "x-requested-with": "XMLHttpRequest",
        "content-length": "0",
    }
    t2c_r = requests.get(url=t2c_url, cookies=cookie, headers=cj_header)
    print(t2c_r.status_code)
    print(t2c_r.text)
    scratch_chances = t2c_r.json()["scratch_chances"]
    return scratch_chances
    # cookies = t2c_r.cookies
    # cookies_dict = str(cookies._cookies)
    # print(cookies._cookies)

