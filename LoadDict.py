'''载入字典文件'''
import pymysql
import re

# 连接到MySQL数据库，MKWEB_PY
db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
cur = db.cursor()

# 重载字典表，若已存在则删除重新加载
cur.execute("drop table if exists DictTable;")
cur.execute("create table DictTable \
    (id int primary key auto_increment, \
    word char(32) not null, \
    interpret text not null)charset=utf8;")

with open(r'.\dict.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        word = re.findall(r'^\S*', line)[0]
        word = word.replace("\'", "\'\'")
        interpret = line[len(word):].lstrip()[:-1]
        interpret = interpret.replace("\'", "\'\'")
        interpret = interpret.replace("\\", "\\\\")

        insert_info = '''insert into DictTable values (0, '%s', '%s');''' % (word, interpret)
        # print(insert_info)

        cur.execute(insert_info)

# cur.execute("insert into DictTable values \
#     (1, 'testword', 'testParaphrase');")

# cur.execute("select * from DictTable;")
# data = cur.fetchall()
db.commit()
cur.close()
db.close()






