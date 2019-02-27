import pymysql

def search_word(word)：
    db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    cur = db.cursor()
    selectinfo = "select interpret from UserInfo where word = \'%s\';" % word
    cur.execute(selectinfo)
    interpret = cur.fetchone()
    db.commit()
    cur.close()
    db.close()  
    return interpret[0]