'''载入字典文件'''
import pymysql
import re

db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
cur = db.cursor()

cur.execute("drop table if exists DictTable;")
cur.execute("create table DictTable \
    (id int primary key, \
    word char(30), \
    Paraphrase varchar(500))charset=utf8;")
i = 0
with open(r'.\dict.txt') as f:
    while True:
        i += 1
        line = f.readline()
        if not line:
            break
        word = re.findall(r'^\S*', line)[0]
        word = word.replace("\'", "\'\'")
        paraphrase = line[len(word):].lstrip()[:-1]
        paraphrase = paraphrase.replace("\'", "\'\'")
        paraphrase = paraphrase.replace("\\", "\\\\")

        insert_info = '''insert into DictTable values (%d, '%s', '%s');''' % (i, word, paraphrase)
        # print(insert_info)

        cur.execute(insert_info)

# cur.execute("insert into DictTable values \
#     (1, 'testword', 'testParaphrase');")

# cur.execute("select * from DictTable;")
# data = cur.fetchall()
db.commit()
cur.close()
db.close()






