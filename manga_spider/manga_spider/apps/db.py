import pymysql

# 创建对象
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root')
cursor = conn.cursor()
def myInsert(comic):
    try:
        sql = ("insert into "
               "comic(name,trans_name,detail_link,cover_img,latest,status,styles,trans_source) "
               "values"
               "(%s,%s,%s，%s,%s,%s，%s,%s,%s,%s)")  # 要插入的数据
        cursor.executemany(sql, comic)  # 执行插入数据

        conn.commit()
        cursor.close()
        conn.close()
        print('insert ok')
    except Exception as e:
        print(e)
