# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import socket
import getopt
import threading
import subprocess

#define global val
listen      = False
command     = False
upload      = False
execute     = ""
target      = ""
upload_destination = ""
port        = 0

def usage():
    print("BHP Tool")
    print("")
    print("Usage:netcat.py -t target_host -p port")

    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()
        pass
    pass

    try:
        opts,args = getopt.getopt(sys.argv[1:],"hel:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        pass

    for o,a in opts:
        if o in ("-h","--help")
            usage()
            pass
        elif o in ("-l","--listen")
            listen = True
        elif o in ("-e","--execute")
            execute = a
        elif o in ("-c","--commandshell")
            command = True
        elif o in ("-u","--upload")
            upload_destination = a
        elif o in ("-t","--target")
            target = a
        elif o in ("-p","--port")
            port = int(a)
        else:
            assert False,"Unhandled Option"

    if not listen and len(target) and port > 0:

        buffer = sys.stdin.read()

        client_sender(buffer)

    if listen:
        server_loop()

main()
