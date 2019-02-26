import socket
import sys
import signal


HOST = '172.16.15.29'
PORT = 8888
ADDR = (HOST, PORT)

server = socket.socket()
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(ADDR)
server.listen(30)

# 处理子进程退出
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

while True:
    confd, addr = server.accept()
    print('%s connected...' % addr)

...