from peewee import *

database = MySQLDatabase('mobile', **{'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': 'wearetvxq5'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

#mobile
class Jiangpin(BaseModel):
    jiangpin = CharField(null=True)
    mobile = CharField(null=True)
    time = DateTimeField(null=True)

    class Meta:
        db_table = 'jiangpin'

class Mobile(BaseModel):
    mobile = CharField(null=True)
    token = CharField(null=True)
    sessionid = CharField(null=True)

    class Meta:
        db_table = 'mobile'



#beauty

class Gallery(BaseModel):
    insert_time = IntegerField()
    gallery_id = CharField()
    title = CharField()
    domain = CharField()
    tags = CharField()
    from_id = CharField()
    all_page = IntegerField()
    publish_time = IntegerField()

    class Meta:
        db_table = 'gallery'

class Image(BaseModel):
    order = IntegerField()
    image_url = CharField()
    title = CharField()
    desc = CharField()
    gallery_id = CharField()

    class Meta:
        db_table = 'image'


if __name__ == '__main__':

    # f = open("/home/sc/Music/quin/mobilesum.py")
    #     #
    # ip_list = []
    #     #
    # for line in f:
    #     print(line)
    #     print(len(line))
    #     if len(line)==12:
    #         line=line.replace('\n','')
    #         ip_list.append(line)
    # f.close()
    # print(ip_list)
    #
    # for i in ip_list:
    #     Mobile.create(
    #         mobile=i
    #     )
    # data=Mobile.select().where(Mobile.id > 1)[0:10]
    # for i in data:
    #     print(i.mobile)
    from datetime import datetime

    Jiangpin.create(
        jiangpin=8,
        mobile=18696100212,
        time= datetime.now()
    )
    # class Jiangpin(BaseModel):
    #     jiangpin = CharField(null=True)
    #     mobile = CharField(null=True)
    #     time = DateTimeField(null=True)

