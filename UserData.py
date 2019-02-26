
'''存储用户信息'''
import pymysql

# 存入单个用户信息
def restore_info(username, password):
    db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    cur = db.cursor()

    cur.execute("create table if not exists UserInfo \
        (UserId char(20), \
        password char(20), \
        unique(UserId))charset=utf8;")
    insertinfo = "insert into UserInfo values ('%s', '%s');" % (username, password)
    cur.execute(insertinfo)
    db.commit()
    cur.close()
    db.close()  

# restore_info('kzsl2018', '89085012')

# 重置用户信息表
def reset_info():
    db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    cur = db.cursor()

    cur.execute("delete from UserInfo;")
    db.commit()
    cur.close()
    db.close()  