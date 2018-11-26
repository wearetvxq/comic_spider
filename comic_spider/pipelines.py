# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ComicSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    collection_name = 'comic'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update({'img_url': item['img_url']}, {'$set': item}, True)
        return item


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi





class MysqlTwistedPipeline(object):
    """
    通用的数据库保存Pipeline
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        自定义组件或扩展很有用的方法: 这个方法名字固定, 是会被scrapy调用的。
        这里传入的cls是指当前的class
        """
        db_parms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接池ConnectionPool
        dbpool = adbapi.ConnectionPool("MySQLdb", **db_parms)

        # 此处相当于实例化pipeline, 要在init中接收。
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将mysql插入变成异步执行
        参数1: 我们每个item中自定义一个函数,里面可以写我们的插入数据库的逻辑
        """
        print('!!!!!!!!')
        print(item)

        query = self.dbpool.runInteraction(self.do_insert, item)


    def do_insert(self, cursor, item):
        """
        执行具体的插入
        根据不同的item 构建不同的sql语句并插入到mysql中
        """

        insert_sql = """
                        insert into tour (title, href, startTime, endTime, host) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
        params = (
            item['title'][0],
            item["href"][0],
            item["startTime"][0],
            item["endTime"][0],
            item["host"][0]
        )
        cursor.execute(insert_sql, params)


