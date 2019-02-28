import pymysql

def search_word(word):
    db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    cur = db.cursor()
    selectinfo = "select interpret from DictTable where word = \'%s\';" % word
    cur.execute(selectinfo)
    interpret = cur.fetchone()
    # print(interpret)
    db.commit()
    cur.close()
    db.close()  
    if not interpret:
        print('Didn\'t find this word, please make sure your spelling right')
        return
    else:
        return interpret[0]