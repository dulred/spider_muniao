import pymysql
import pandas as pd
import os
import sys

# 加入可识别的路径 PYTHONPATH
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

sys.path.append(parent_directory)


from utils.directory_utils import DirectoryUtils as Du
# 爬取的文件夹
dir_utils = Du()
open_path = dir_utils.get_path('data', 'clean.csv')




try:
    # 创建 MySQL 连接对象
    conn = pymysql.connect(
            host = '192.168.1.26',
            user = 'root',
            password = '123456',
            db = 'spider_room',
            charset = 'utf8'
        )
    
    # 连接成功，打印连接信息
    print("Connection successful!")
    print("MySQL server info:", conn.get_server_info())
    cur = conn.cursor()

    # 关闭连接
    # conn.close()
except pymysql.Error as e:
    # 连接失败，打印错误信息
    print("Error connecting to MySQL:", e)

def data():
    df = pd.read_csv(open_path)
    
    create_table_sql = """
        create table if not exists data(
            id int primary key AUTO_INCREMENT,
            name varchar(255),
            score varchar(255),
            hx varchar(255),
            home_type varchar(255),
            kz varchar(255),
            price varchar(255),
            img_url varchar(255),
            city varchar(255)
        )
    """
    cur.execute(create_table_sql)

    insert_sql = 'insert into data(name,score,hx,home_type,kz,price,img_url,city) values(%s,%s,%s,%s,%s,%s,%s,%s)'
    for index,row in df.iterrows():
        cur.execute(insert_sql,tuple(row))
    
    conn.commit()
    cur.close()
    conn.close()

data()