#!/usr/bin/env python3


import socket
import os

target_host = "www.baidu.com"
target_port = 80
request = "GET / HTTP/2.0\r\nHost: baidu.com\r\n\r\n"
request = str.encode(request)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))

client.send(request)

response = client.recv(4096)

print(response)
