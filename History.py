
'''存储用户查询记录'''
import pymysql

# 重置查询记录
def reset_info():
    db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    cur = db.cursor()

    cur.execute("drop table if exists History;")
    cur.execute("create table History \
    (Id int primary key auto_increment, \
    UserId char(20), \
    word char(20), \
    time datetime, \
    index(UserId))charset=utf8;")
    db.commit()
    cur.close()
    db.close()  

# reset_info()