import socket
import sys
import time

import Dict

# 登陆成功，可查询单词
def working():
    while True:
        word = input('[word: ]\n<<<  ')
        if not word:
            break
        interpret = Dict.search_word(word)
        if not interpret:
            continue
        print('[Interpret: ]\n>>>  ', interpret)

client = socket.socket()
HOST = '172.16.15.29'
PORT = 8888
ADDR = (HOST, PORT)
try:
    client.connect(ADDR)
except:
    print('[Error: ]Connect failed, client will be closed after 5 second')
    time.sleep(5)
    sys.exit('Bye')

print('+----------------------------------+')
print('|            PudgeDict             |')
print('|                        --ver 1.0 |')
print('|                                  |')
print('|        Sign In or Sign Up        |')
print('+----------------------------------+')

while True:
    sign = input('Sign In(I) or Sign Up(U):')
    if sign == 'I':
        username = input('[Please input your username:]\n<<<  ')
        password = input('[Please input your password:]\n<<<  ')
        msg = 'signin#%s#%s' % (username, password)
        # print(msg)
        client.send(msg.encode())
        data = client.recv(1024).decode()
        # print(data)
        if data == 'Success':
            print('[Welcome!!]', username)
            working()
            print('[Bye]', username)
            break
        elif data == 'Failed':
            print('[Error: ]Your password was wrong, please try again!!')
            continue

    elif sign == 'U':
        username = input('[Please set your username:]\n<<<  ')
        password = input('[Please set your password:]\n<<<  ')
        password2 = input('[Please repeat your password:]\n<<<  ')
        if password != password2:
            print('[Error: ]password don\'t match')
            continue
        msg = 'signup#%s#%s' % (username, password)
        client.send(msg.encode())
        sign = 'I'
        
    elif sign == 'Q':
        client.close()
        sys.exit('[Bye]')
    else:
        print('[Error: ]Wrong input!!')
        continue

client.close()