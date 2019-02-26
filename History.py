
'''存储用户查询记录'''
import pymysql

# 存入单次查询记录
def restore_info(username, word):
    db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    cur = db.cursor()

    cur.execute("create table if not exists History \
        (Id int primary key auto_increment, \
        UserId char(20), \
        word char(20), \
        time datetime, \
        index(UserId))charset=utf8;")
    insertinfo = "insert into History values (0, '%s', '%s', now());" % (username, word)
    cur.execute(insertinfo)
    db.commit()
    cur.close()
    db.close()  

# 重置查询记录
def reset_info():
    db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    cur = db.cursor()

    cur.execute("delete from History;")
    db.commit()
    cur.close()
    db.close()  

reset_info()