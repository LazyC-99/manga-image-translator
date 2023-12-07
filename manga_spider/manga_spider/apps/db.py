import os

import pymysql
from googletrans import Translator


class Database:
    def __init__(self, host="127.0.0.1", user="root", password="", database="comic"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection.open:
            self.cursor.close()
            self.connection.close()

    def insert_comic(self, item):
        self.connect()
        try:

            sql = ("insert into comic"
                   "(name,trans_name,detail_link,cover_img,latest,status,styles) "
                   "values"
                   "(%s,%s,%s,%s,%s,%s,%s)")  # 要插入的数据
            # 翻译漫画名
            translator = Translator()
            translation = translator.translate(item['name'], dest='zh-cn').text
            values = (item['name'], translation, item['detail_link'], item['img'],
                      item['latest'], item['status'], ', '.join(item['styles']))
            self.cursor.execute(sql, values)  # 执行插入数据
            self.connection.commit()
            self.disconnect()
            print(f'新增{item["name"]}')
        except Exception as e:
            self.disconnect()
            print(e)

    def update_chapter(self, name, chapter):
        self.connect()
        try:
            sql = "update comic set download = %s where name = %s"
            values = (chapter, name)
            self.cursor.execute(sql, values)  # 执行插入数据
            self.connection.commit()
            self.disconnect()
            print(f"新下章节{chapter}")
        except Exception as e:
            self.disconnect()
            print(e)

    def select_by_name(self, comic_name):
        self.connect()
        try:
            sql = "select * from comic where name = %s"
            self.cursor.execute(sql, comic_name)  # 执行插入数据
            result = self.cursor.fetchall()
            self.connection.commit()
            self.disconnect()
            return result[0]
        except Exception as e:
            self.disconnect()
            print(e)

    def update_comic(self, manga_item):
        self.connect()
        try:
            sql = "update comic set latest = %s where name = %s"
            values = (manga_item['latest'], manga_item['name'])
            self.cursor.execute(sql, values)  # 执行插入数据
            self.connection.commit()
            self.disconnect()
            print(f"{manga_item['name']}已更新")
        except Exception as e:
            self.disconnect()
            print(e)

    def update_by_dir(self, path):
        # 获取指定路径下的所有文件和文件夹
        entries = os.scandir(path)

        # 筛选出文件夹
        subfolders = [entry.name for entry in entries if entry.is_dir()]

        return subfolders


if __name__ == '__main__':
    db = Database()
    by_name = db.update_by_dir("C:/Users/Administrator/Desktop/image")
    print(by_name)
