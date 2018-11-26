# -*- coding: utf-8 -*-
import scrapy,re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WhkxSpider(scrapy.Spider):

    def Replace(self,text):
        text=text.replace(" ","")
        text = text.replace("\xa0", "")
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = text.replace(" ", "")
        text = text.replace(":", "：")
        return text
    name = 'whkx'
    # allowed_domains = ['kjj.wuhan.gov.cn/xmsbygl/index.jhtml']
    start_urls = ['http://kjj.wuhan.gov.cn/xmsbygl/index.jhtml']
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    def parse(self,response):
        for i in range(4):
            url = 'http://kjj.wuhan.gov.cn/xmsbygl/index_{}.jhtml'.format(str(i+1))
            driver = webdriver.Chrome(chrome_options=self.chrome_options)
            driver.get(url)
            data = driver.page_source
            soup = BeautifulSoup(data, 'lxml')
            links=soup.select('div.list_news.clearfix > ul')
            # print(links)
            for link in links:
                # link=link.select('ul > li > a')[0].get('href')
                link= link.select(' a ')[0].get('href')
                print(link)

                yield self.parse_content(link)
                pass




    def parse_content(self,url):
        driver = webdriver.Chrome(chrome_options=self.chrome_options)
        driver.get(url)
        data = driver.page_source
        soup = BeautifulSoup(data, 'lxml')
        infolist={}
        infolist['title'] = soup.select('div.art_title > h4')[0].get_text()
        try:
            infolist['release'] =soup.select('div.info > span:nth-of-type(1)')[0].get_text().replace('发布时间：','')
        except:
            infolist['release']='0'
        infolist['source']='武汉市科学技术局'
        infolist['original']=url
        try:
            infolist['total']=soup.select('div.info > span:nth-of-type(2)')[0].get_text().replace('浏览：','')
        except:
            infolist['total'] ='0'
        infolist['content']=str(soup.select('div#txt')[0])
        p_list=soup.select('#txt')[0].find_all('p')

        infolist['declare'] = '0'
        infolist['deadline'] = '0'
        try:
            for p in p_list:
                if '受理时间' in p.text:
                    # print(p.text)
                    infolist['declare']=re.findall(r'\d{4}年\d{1,2}月\d{1,2}日',p.text)[0]
                    infolist['deadline']=re.findall(r'\d{4}年\d{1,2}月',p.text)[0]+re.findall(r'\d{1,2}日',p.text)[1]
                    break

        except:
            infolist['declare']='0'
            infolist['deadline']='0'


        try:
            for i in range(len(p_list)):
                if '申报时间' in p_list[i].text:
                    for x in range(2):
                        try:

                            infolist['declare']=re.findall('\d{4}年\d{1,2}月\d{1,2}日',p_list[i+x].text)[0]
                            # print(infolist['declare'])
                            infolist['deadline']=re.findall('\d{4}年',p_list[i+x].text)[0]+re.findall('\d{1,2}月\d{1,2}日',p_list[i+x].text)[1]
                            # print(infolist['deadline'])
                            break
                        except:
                            infolist['declare'] = '0'
                            infolist['deadline'] = '0'
        except:
            infolist['declare'] = '0'
            infolist['deadline'] = '0'

        infolist['contact'] = '0'
        infolist['phone'] = '0'
        # 时间
        for i in range(len(p_list)):
            if self.Replace(p_list[i].text).find('截止时间') != -1 or self.Replace(p_list[i].text).find('截止日期') != -1:
                try:
                    infolist['deadline'] = re.findall(r'截止.*?日', p_list[i].text)[0].replace('：', '')
                    break
                except:
                    infolist['deadline'] = '0'
        # 电话
        for i in range(len(p_list)):
            if self.Replace(p_list[i].text).find('联系方式：') != -1 or self.Replace(p_list[i].text).find(
                    '联系人：') != -1 or self.Replace(p_list[i].text).find('电话：') != -1 or self.Replace(
                p_list[i].text).find('联系电话：') != -1:
                try:
                    phone = re.findall(r'[\：].*', p_list[i].text)[0].replace('：', '')
                    infolist['phone'] = re.findall('\d+-{0,1}\d+', phone)[0]
                    # print(infolist['phone'])
                    break
                except:
                    infolist['phone'] = '0'
        # 联系人
        for i in range(len(p_list)):
            if self.Replace(p_list[i].text).find('联系人：') != -1 or self.Replace(p_list[i].text).find('负责人：') != -1:
                try:
                    infolist['contact'] = re.findall(r'[\：].*', p_list[i].text)[0].replace('：', '')
                    infolist['contact'] = infolist['contact'].replace('电话', '').replace('-', '').replace('1',
                                                                                                         '').replace(
                        '2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7',
                                                                                                             '').replace(
                        '8', '').replace('9', '').replace('0', '')
                    break
                except:
                    infolist['contact'] = '0'
        # 附件
        for i in range(len(p_list)):
            if self.Replace(p_list[i].text).find('附件：') != -1:
                try:
                    infolist['url'] = p_list[i].select('a')[0].get('href')
                    break
                except:
                    infolist['url'] = '0'

        try:
            infolist['url'] = 'http://kjj.wuhan.gov.cn'+soup.select('div#txt')[0].select('a')[0].get('href')
        except:
            infolist['url']='0'




        print(infolist)

        return infolist



