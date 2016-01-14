#!/usr/bin/env python3

import socket

localIP = socket.gethostbyname(socket.gethostname())
while True:
    print ("Enter the IP of the machine you will be "
        "communicating with. (Default Local IP: '{}')" 
        .format(str(localIP)), end="")
    TCP_IP = input(" >> ") or localIP
    try:
        socket.inet_aton(TCP_IP)
        # Legal
        break
    except socket.error:
        # Not Legal
        print("You need to enter a valid IPv4 address!\n")
        continue
#TCP_IP = raw_input('Enter IPv4 address of Recipient: ')
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((localIP, TCP_PORT))
s.bind((TCP_IP,TCP_PORT))
s.listen(1)

conn, addr = s.accept()

print("Connection Address: " + addr)

while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("Received data: " + data)
    conn.send(data) #echo

conn.close()
