##bring in the GPIO Header File.
#We will have to bring in the COM header as well
import RPi.GPIO as GPIO
import time
import sys
import struct
import socket
#set up the GPIO using BCM Numbering
GPIO.setmode(GPIO.BCM)

#Define the I/O pins
GPIO.setup(17, GPIO.OUT) #PIN 11 on board (RED)

GPIO.setup(04, GPIO.OUT) #PIN 7 on board (Green)


#PIN 9 is ground

#COM protocols

# Setup connection to other Pi
# Prompt for IP. Default localhost if null input
#
UDP_IP = input("Enter the IP of the client machine you will be communicating with. (Default: '127.0.0.1')>$

# Prompt for PORT. Default 65104 if null input
#   
while True:
    try:
        UDP_PORT = int(input("Enter the PORT you will be communicating over. (Default: 65104)>> ") or '651$
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
sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM) # Receive over internet using UDP
sock.bind((UDP_IP, UDP_PORT))

# Prompt user we are now monitoring for messages
#
print("Program is now monitoring {}:{} for messages" .format(str(UDP_IP), UDP_PORT))
while True:
    print ("Waiting for Message")
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data =  bytes.decode(data, 'UTF-8')

    print ("received message: {}" .format(data))


	
	if data == 'r':
	
		GPIO.output(17, 1);
		time.sleep(3);
		GPIO.output(17, 0);
	
	elif data == 'g':
	
		GPIO.output(04, 1);
		time.sleep(3);
		GPIO.output(04, 0);
	
	elif data == 'stop':
	
		#Reset the GPIO before exiting
		GPIO.cleanup;
		print('Communications have ended successfully\n');
	
		sys.exit();
	
	else:
		print('No valid LED selected');
		time.sleep(2);	
	
	
