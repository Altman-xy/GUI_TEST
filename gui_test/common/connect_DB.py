import pymysql

class DBtools:
    def __init__(self):
        self.db=pymysql.connect(host='localhost',user='root',password='',database='aileone',charset='utf8')
        self.cursor=self.db.cursor()     #获取游标
