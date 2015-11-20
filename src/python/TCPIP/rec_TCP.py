#!/usr/bin/env python

import socket

TCP_IP = raw_input('Enter IPv4 address of Recipient: ')
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.bind((TCP_IP,TCP_PORT))
s.listen(1)

conn, addr = s.accept()

print "Connection Address: ", addr

while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data: ", data
    conn.send(data) #echo

conn.close()
