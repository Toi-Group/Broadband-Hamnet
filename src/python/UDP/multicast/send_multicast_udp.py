#!/usr/bin/env python3
#
# Source: https://pymotw.com/2/socket/multicast.html
#
import socket
import struct
import sys

MESSAGE = 'very important data'
MESSAGE = bytes(MESSAGE, 'UTF-8')
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
sock.settimeout(0.2)
# to receive data.

# Set the time-to-live for MESSAGEs to 3 so they do go three routers past
# local network segment.
ttl = struct.pack('b', 64)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:

    # Send data to the multicast group
    print('sending' + bytes.decode(MESSAGE, 'UTF-8'))
    sent = sock.sendto(MESSAGE, multicast_group)

    # Look for responses from all recipients
    while True:
        print('waiting to receive...')
        try:
            data, server = sock.recvfrom(16)
            data =  bytes.decode(data, 'UTF-8')
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print ("received message: {}" .format(data))

finally:
    print('closing socket')
    sock.close()