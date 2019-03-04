import socket
import sys
import time
import pymysql

# 查询单词
def search_word(word):
    '''输入：单词， 返回：释义或空值'''

    selectinfo = "select interpret from DictTable where word = \'%s\';" % word
    cur.execute(selectinfo)
    interpret = cur.fetchone()
    db.commit()

    if not interpret:
        return
    else:
        return interpret[0]

# 存入单次查询记录
def restore_info(username, word):

    insertinfo = "insert into History values (0, '%s', '%s', now());" % (username, word)
    cur.execute(insertinfo)
    db.commit()


# 查询历史
def show_record(username):
    selectinfo = "select * from History where UserId = \'%s\';" % username
    cur.execute(selectinfo)
    record = cur.fetchall()
    db.commit()
    for re in record:
        print('%s, %10s, %s' % (re[1], re[2], re[3]))

# 登陆成功，工作状态，可查询单词
def working():
    while True:
        word = input('[请输入单词: ]\n<<<  ')
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
            print('未查询到此单词')
            continue
        restore_info(username, word)
        print('[单词释义: ]\n>>>  ', interpret)
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
    sign = input('登录(I) or 注册(U):')
    # 登录
    if sign == 'I':
        username = input('[请输入用户名:]\n<<<  ')
        password = input('[请输入密码:]\n<<<  ')
        msg = 'signin#%s#%s' % (username, password)
        client.send(msg.encode())
        data = client.recv(1024).decode()
        if data == 'Success':
            print('[Welcome!!]', username)
    # 连接数据库
            db = pymysql.connect('172.16.10.124', 'root', 'root', database = 'MKWEB_PY', charset='utf8')
            cur = db.cursor()
            print('[#Q 退出, #L 注销, #H 查询历史]')
            # 工作状态
            state = working()
            if state == '#L':
                # 返回登录界面
                continue
            elif state == '#Q':
                print(['Bye'], username)
                cur.close()
                db.close()
                break
            elif state == '#H':
                show_record(username)
                continue

        elif data == 'False':
            print('[Error: ]密码错误')
        else:
            print('[Error: ]请重试')
        continue
    # 注册
    elif sign == 'U':
        username = input('[请设置用户名:]\n<<<  ')
        password = input('[请设置密码:]\n<<<  ')
        password2 = input('[请重新输入密码:]\n<<<  ')
        if password != password2:
            print('[Error: ]两次密码不一致')
            continue
        msg = 'signup#%s#%s' % (username, password)
        client.send(msg.encode())
        data = client.recv(1024).decode()
        if data == 'signup#success':
            print('注册成功')

# 退出方式2：登录界面输入Q
    # 关闭数据库
    elif sign == 'Q':
        cur.close()
        db.close()
        break
        
    else:
        print('[Error: ]输入有误')
        continue

# 循环中止-客户端退出
# 发送退出信息给服务器等待回收
quitmsg = 'quit#%s' % username
client.send(quitmsg.encode())
client.close()
sys.exit('[Bye]')