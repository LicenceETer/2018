# -*- coding: utf-8 -*-
#!/usr/bin/env python


def client_handler(buffer):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)

        while true:
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
                pass
            print(response)
            pass

            buffer = raw_input("")
            buffer += "\n"
        pass

    except:
        print("[*] Exception! Exiting.")
        client.close()
        raise
    pass


def server_loop():
    global server

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))

    server.listen(5)

    while True:
        client_socket,addr = server.accept()

        client_thread = threading.Thread(target=client_handler,args=(clietn_socket,))
        client_thread.start()
    pass

def run_command(command):

    command = command.rstrip()

    try:
        output = subprocess.check_output(command.stderr=subprocess.STDOUT,shell=True)
    except:
        output = "Failed to execute command.\r \n"

    return output
    pass
