# -*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9999
bind_addr = (bind_ip,bind_port)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(bind_addr)
TypeError: getsockaddrarg: AF_INET address must be tuple, not str
server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip,bind_port))


def handle_client(client_socket):

    request = client_socket.recv(4096)

    print("[*] Received:%s " % request)

    client_socket.send("ACK!")

    client_socket.close()

while True:
    client,addr = server.accept()

    print("[*] Accepted connection from: %s %d" % (addr[0],addr[1]))

    client_handler = threading.Thread(target=handle_client,args=client)
    client_handler.start()
    pass
