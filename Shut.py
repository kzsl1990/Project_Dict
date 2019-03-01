import socket
import sys


# 定义全局变量，创建客户端套接字
client = socket.socket()
HOST = '172.16.15.29'
PORT = 8888
ADDR = (HOST, PORT)

client.connect(ADDR)
client.close()
sys.exit('[Bye]')
