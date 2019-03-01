import socket
import sys
import time
import pymysql

# 查询单词
def search_word(word):
    '''输入：单词， 返回：释义或空值'''
    # db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    # cur = db.cursor()
    selectinfo = "select interpret from DictTable where word = \'%s\';" % word
    cur.execute(selectinfo)
    interpret = cur.fetchone()
    db.commit()
    # cur.close()
    # db.close()  
    if not interpret:
        return
    else:
        return interpret[0]

# 存入单次查询记录
def restore_info(username, word):
    # db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
    # cur = db.cursor()

    # cur.execute("create table if not exists History \
    #     (Id int primary key auto_increment, \
    #     UserId char(20), \
    #     word char(20), \
    #     time datetime, \
    #     index(UserId))charset=utf8;")
    insertinfo = "insert into History values (0, '%s', '%s', now());" % (username, word)
    cur.execute(insertinfo)
    db.commit()
    # cur.close()
    # db.close()  

# 查询历史
def show_record(username):
    pass

# 登陆成功，工作状态，可查询单词
def working():
    while True:
        word = input('[word: ]\n<<<  ')
        # 特殊指令，终止工作状态，返回指令
        if (word == '#Q') or (word == '#L') or (word == '#H'):
            break
        # 输入为空则重新输入
        if not word:
            continue
        # 有效输入，进行查询
        interpret = search_word(word)
        # 未查询到结果
        if not interpret:
            print('Didn\'t find this word, please make sure your spelling right')
            continue
        restore_info(username, word)
        print('[Interpret: ]\n>>>  ', interpret)
    return word

# 定义全局变量，创建客户端套接字
client = socket.socket()
HOST = '172.16.15.29'
PORT = 8888
ADDR = (HOST, PORT)

try:
    client.connect(ADDR)
except:
    print('[Error: ]Connect failed, client will be closed')
    client.close()
    sys.exit('[Bye]')

# 登录界面
print('+----------------------------------+')
print('|            PudgeDict             |')
print('|                        --ver 1.0 |')
print('|                                  |')
print('|        Sign In or Sign Up        |')
print('+----------------------------------+')

while True:
    sign = input('Sign In(I) or Sign Up(U):')
    # 登录
    if sign == 'I':
        username = input('[Please input your username:]\n<<<  ')
        password = input('[Please input your password:]\n<<<  ')
        msg = 'signin#%s#%s' % (username, password)
        client.send(msg.encode())
        data = client.recv(1024).decode()
        if data == 'Success':
            print('[Welcome!!]', username)
    # 连接数据库
            db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
            cur = db.cursor()
            print('[#Q for quit, #L for login page, #H for history]')
            # 工作状态
            state = working()
            if state == '#L':
                # 返回登录界面
                continue
            elif state == '#Q':
                print(['Bye'], username)
# 退出方式1：查询状态输入#Q
    # 关闭数据库
                cur.close()
                db.close()
                break
            elif working() == '#H':
                show_record(username)

        elif data == 'False':
            print('[Error: ]Wrong password')
        else:
            print('[Error: ]Your password was wrong, please try again!!')
        continue
    # 注册
    elif sign == 'U':
        username = input('[Please set your username:]\n<<<  ')
        password = input('[Please set your password:]\n<<<  ')
        password2 = input('[Please repeat your password:]\n<<<  ')
        if password != password2:
            print('[Error: ]password don\'t match')
            continue
        msg = 'signup#%s#%s' % (username, password)
        client.send(msg.encode())
        data = client.recv(1024).decode()
        if data == 'signup#success':
            print('Sign up successful')

# 退出方式2：登录界面输入Q
    # 关闭数据库
    elif sign == 'Q':
        cur.close()
        db.close()
        break
        
    else:
        print('[Error: ]Wrong input!!')
        continue

# 循环中止-客户端退出
# 发送退出信息给服务器等待回收
quitmsg = 'quit#%s' % username
client.send(quitmsg.encode())
client.close()
sys.exit('[Bye]')