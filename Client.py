import socket
import sys
import time

import Dict

# 登陆成功，可查询单词
def working():
    while True:
        word = input('word: ')
        if not word:
            break
        interpret = Dict.search_word(word)
        print('interpret: ', interpret)

client = socket.socket()
HOST = '172.16.15.29'
PORT = 8888
ADDR = (HOST, PORT)
try:
    client.connect(ADDR)
except:
    print('Connect failed, client will be closed after 5 second')
    time.sleep(5)
    sys.exit('Bye')

print('+------------------------+')
print('|       PudgeDict        |')
print('|              --ver 1.0 |')
print('|                        |')
print('|   Sign In or Sign Up   |')
print('+------------------------+')

sign = input('Sign In(I) or Sign Up(U):')
while True:
    if sign == 'I':
        username = input('please input your username:')
        password = input('please input your password:')
        msg = 'signin#%s#%s' % (username, password)
        client.send(msg.encode())
        data = client.recv(1024).decode()
        if data == 'Success':
            print('Welcome!!')
            working()
            break
        elif data == 'Failed':
            print('Your password was wrong, please try again!!')
            continue

    elif sign == 'U':
        username = input('please set your username:')
        password = input('please set your password:')
        password2 = input('please repeat your password:')
        if password != password2:
            print('password don\'t match')
            continue
        msg = 'signup#%s#%s' % (username, password)
        client.send(msg.encode())
        
    elif sign == 'Q':
        client.close()
        sys.exit('Bye')
    else:
        print('Wrong input!!')
        continue

client.close()