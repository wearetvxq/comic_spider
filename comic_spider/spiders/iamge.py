import time

from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver.common.by import By
# -*- coding: utf-8 -*-
import scrapy,re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')




# data = driver.page_source


url = "http://www.ccba.org.cn/index.aspx"
# 1、打开浏览器，最大化浏览器
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)
driver.implicitly_wait(10)
driver.maximize_window()

# 用户名元素
userElement = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/input")
# 密码元素
passElement = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/input")
# 验证码输入框元素
codeElement = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr/td[2]/table/tbody/tr[3]/td[2]/input")
# 验证图片元素
imgElement = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr/td[2]/table/tbody/tr[4]/td/img")

# 2、截取屏幕内容，保存到本地
driver.save_screenshot("./test/01.png")


# 3、打开截图，获取验证码位置，截取保存验证码
ran = Image.open("./test/01.png")
box = (1120, 280, 1180, 310)  # 获取验证码位置,自动定位不是很明白，就使用了手动定位，代表（左，上，右，下）
ran.crop(box).save("./test/02.png")
driver.close()