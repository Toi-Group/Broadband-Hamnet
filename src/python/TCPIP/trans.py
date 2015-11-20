#!/usr/bin/env python

import socket
from threading import Thread
import sys



def receiveTCP():
    TCP_IP = raw_input('Enter IPv4 of this Machine: ')

    #port this machine listens on
    #this needs to be the send port of other machine
    #
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    
    #create a tuple with port and ip
    DEST = (TCP_IP, TCP_PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((DEST))
    s.listen(1)
   
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if data == 'EXIT':
            sys.exit()

        print "received data:", data
        conn.send(data)  # echo
   

def sendTCP():
    TCP_IP = raw_input('Enter IPv4 address of Recipient: ')
    #This is the port we will send to on the listening machine
    #this port needs to be 8888 on receiving side
    TCP_PORT = 8888
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    while 1:

        MESSAGE = raw_input("Enter Message: ")

        #send the message
        s.send(MESSAGE)
        if MESSAGE == "EXIT":
            sys.exit()
        
        #listen for confirmation
        response = s.recv(BUFFER_SIZE)
        if response != None:
            print "%s received message: %s" % (TCP_IP, response)
        
    #if we get the exit message, close the connection


def main():
    #start a thread to receive
    #
    R = Thread(target=receiveTCP)
    S = Thread(target=sendTCP)

    R.start()
    S.start()

if __name__ == '__main__':
    main()

