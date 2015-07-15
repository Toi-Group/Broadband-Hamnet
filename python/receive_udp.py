# !python3
#

# Source: https://wiki.python.org/moin/UdpCommunication
#

# This code receives a message from a UDP_IP source running the script 
# send_udp.py
#

import socket

# Setup connection to other Pi
#
UDP_IP = str(input("Enter the IP of the client machine you will be communicating with. (Ex. '127.0.0.1'): "))
UDP_PORT = int(input("Enter the PORT you will be communicating over. (Ex. 5005): "))

sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM) # Receive over internet using UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print ("received message: {}" .format(data))