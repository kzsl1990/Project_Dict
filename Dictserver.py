# import socket
from socket import * 
import sys
# import signal 
from signal import * 
import threading

import UserData


def Handler(confd, addr):
    while True:
        logindata = confd.recv(1024).decode()
        logindata = logindata.split('#')
        if logindata[0] == 'signup':
            username = logindata[1]
            password = logindata[2]
            UserData.restore_info(username, password)
            msg = 'signup#success'
            confd.send(msg.encode())
        elif logindata[0] == 'signin':
            username = logindata[1]
            password = logindata[2]
            if password == UserData.match_info(username):
                msg = 'Success'
                confd.send(msg.encode())
            else:
                msg = 'Failed'
                confd.send(msg.encode())

HOST = '172.16.15.29'
PORT = 8888
ADDR = (HOST, PORT)

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(ADDR)
server.listen(30)

print('Dict start, waiting for connection...')
# 处理子进程退出
# signal(SIGCHLD, SIG_IGN)
T = []
while True:
    confd, addr = server.accept()
    print(addr, 'connected...')
    t = threading.Thread(target = Handler, args = (confd, addr))
    T.append(t)
    t.start()


for i in T:
    i.join()
