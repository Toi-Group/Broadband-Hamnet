#!/usr/bin/env python

import socket

TCP_IP = raw_input('Enter IP of this Machine: ')
TCP_PORT = 5005
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:

    MESSAGE = s.recv(BUFFER_SIZE)
    if MESSAGE != None:
        print MESSAGE
        MESSAGE = None
