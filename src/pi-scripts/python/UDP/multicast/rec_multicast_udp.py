#!/usr/bin/env python3
#
# Source: https://pymotw.com/2/socket/multicast.html
#
import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    print('waiting to receive message...')
    data, address = sock.recvfrom(1024)
    data =  bytes.decode(data, 'UTF-8')
    
    print('received call from: "' + str(address) + '".')
    print(data)

    print('sending acknowledgement to', str(address))
    MESSAGE_ack = 'ack'
    MESSAGE_ack = bytes(MESSAGE_ack, 'UTF-8')
    sock.sendto(MESSAGE_ack, address)

