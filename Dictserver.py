import socket
# from socket import * 
import sys

import threading

import UserData


def Handler(confd, addr):
    while True:
        logindata = confd.recv(1024).decode()
        logindata = logindata.split('#')
        # 注册
        if logindata[0] == 'signup':
            username = logindata[1]
            password = logindata[2]
            UserData.restore_info(username, password)
            msg = 'signup#success'
            confd.send(msg.encode())
        # 登录
        elif logindata[0] == 'signin':
            username = logindata[1]
            password = logindata[2]
            if UserData.match_info(username) == password:
                msg = 'Success'
            elif UserData.match_info(username) == '':
                msg = 'False'
            else:
                msg = 'Failed'
            confd.send(msg.encode())
        elif logindata[0] == 'quit':
            print(logindata[1], 'quited')
            break

# 设置全局变量
HOST = '172.16.15.29'
PORT = 8888
ADDR = (HOST, PORT)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen(30)

    print('DictServer start, waiting for connection...')
    # 处理子进程退出(windows不可用)
    # signal(SIGCHLD, SIG_IGN)
    T = []
    try:
        while True:
            confd, addr = server.accept()
            print(addr, 'connected...')
            t = threading.Thread(target = Handler, args = (confd, addr))
            T.append(t)
            t.start()
    except KeyboardInterrupt:
        print('Server closed')
        for i in T:
            i.join()
        sys.exit('[Bye]')

if __name__ == '__main__':
    main()
