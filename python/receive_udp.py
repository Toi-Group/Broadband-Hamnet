# !python3
#
# Source: https://wiki.python.org/moin/UdpCommunication
#
# This code receives a message from a UDP_IP source running the script 
# send_udp.py
#

import socket

# Setup connection to other Pi
# Prompt for IP. Default localhost if null input
#
while True:
    UDP_IP = input("Enter the IP of the client machine you will be "
    "communicating with. (Default: '127.0.0.1')>> ") or '127.0.0.1'
    try:
        socket.inet_aton(UDP_IP)
        # Legal
        break
    except socket.error:
        # Not Legal
        print("You need to enter a valid IPv4 address!\n")
        continue
        
# Prompt for PORT. Default 65104 if null input
#   
while True: 
    try:
        UDP_PORT = int(input("Enter the PORT you will be communicating over. "
        "(Default: 65104)>> ") or '65104')
    except ValueError:
        print("You need to type in a valid PORT number!")
        continue
    else:
        if UDP_PORT in range(65535):
            break
        else:
            print("Port must be in range 0-65535!")
            continue

# Bind the socket
#
# Receive over internet using UDP
#
sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))

# Prompt user we are now monitoring for messages
#
print("Program is now monitoring {}:{} for messages" .format(str(UDP_IP), 
    UDP_PORT))
while True:
    print ("Waiting for Message")
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data =  bytes.decode(data, 'UTF-8')
    
    print ("received message: {}" .format(data))