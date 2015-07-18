# !python3
#
# Source: https://wiki.python.org/moin/UdpCommunication
#
# This code sends a message to another script running at the UDP_IP destination
# the script receive_udp.py
#

import socket

# Get local IP
#
localIP = socket.gethostbyname(socket.gethostname())

# Setup connection to other Pi
# Prompt for IP. Default localIP if null input
#
while True:
    print ("Enter the IP of the client machine you will be "
        "communicating with. (Default Local IP: '{}')" 
        .format(str(localIP)), end="")
    UDP_IP = input(" >> ") or localIP
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
            "(Default. 65104) >> ") or '65104')
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
# Send over internet using UDP
#
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 


# Run the program forever
while True:
    # Prompt the user for a keystroke or message to send
    #
    MESSAGE = input("What would you like to send (keyboard input)>> ")
    
    # Let the user know what IP and Port we are using to communicate with
    #
    print ('Sending message to UDP target: {}:{}' .format(str(UDP_IP), 
        UDP_PORT))
    
    # Send the message using the socket opened
    #
    sock.sendto(bytes(MESSAGE, 'UTF-8'), (UDP_IP, UDP_PORT))
    
    # Confirm with the user the message sent succesfully
    #
    print ("Successfully sent message: {}" .format(str(MESSAGE)))