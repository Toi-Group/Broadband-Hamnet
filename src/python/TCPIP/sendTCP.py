#!/usr/bin/env python

import Queue
import socket
from localIP import localIP

#sendTCP
#write what function
#does here, explain
#inputs and outputs
#
def sendTCP(q_send,q_rec):

    #initialize the send queue
    #
    q_send.put(0)

    #get local IPv4
    #
    #TCP_IP = raw_input('Enter IPv4 address of Recipient: ')
    #
    TCP_IP = localIP()
    
    #This is the port we will send to on the listening machine
    #this port needs to be 8888 on receiving side
    #
    TCP_PORT = 5005
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    while 1:

        #Ensure the rec queue is not empty
        #
        if q_rec.empty():
            #if it is empty, put a 0 on the queue
            #
            q_rec.put(0)

        #check the receive thread's status
        #
        check = q_rec.get()
        if check:
            s.close()
            q_send.put(1)
            break

        MESSAGE = raw_input("Enter Message: ")

        #send the message
        #
        s.send(MESSAGE)

        #if we get the exit message, close the socket, signal the receive thread and
        #then let the thread terminate
        #
        if MESSAGE == "EXIT":
            q_send.put(1)
            s.close()
            break

        #if we dont get the exit message, signal the receive thread
        #to continue running
        #else:
        #     q_send.put(0)

        #listen for confirmation
        #response = s.recv(BUFFER_SIZE)
        #if response != None:
        #    print "%s received message: %s" % (TCP_IP, response)
