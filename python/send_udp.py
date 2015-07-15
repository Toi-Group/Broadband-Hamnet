# !python3
#

# Source: https://wiki.python.org/moin/UdpCommunication
#

# This code sends a message to another script running at the UDP_IP destination
# the script receive_udp.py
#

import socket

# Setup connection to other Pi
#
UDP_IP = input("Enter the IP of the client machine you will be communicating with. (Ex. '127.0.0.1'): ")
UDP_PORT = input("Enter the PORT you will be communicating over. (Ex. 5005): ")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Send over internet using UDP


# Run the program forever
while True:
	# Prompt the user for a keystroke or message to send
	#
	MESSAGE = input("What would you like to send (keyboard input) ")
	
	# Let the user know what IP and Port we are using to communicate with
	#
	print ('Sending message to UDP target: {}  using port: {}' .format(str(UDP_IP), str(UDP_PORT)))
	
	# Send the message using the socket opened
	#
	sock.sendto(bytes(MESSAGE, 'UTF-8'), (UDP_IP, UDP_PORT))
	
	# Confirm with the user the message sent succesfully
	#
	print ("Message sent: {}" .format(str(MESSAGE)))