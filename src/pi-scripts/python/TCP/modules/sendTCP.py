#!/usr/bin/env python3

import socket

#sendTCP
#write what function
#does here, explain
#inputs and outputs
#
def sendTCP(TCP_IP, q_send,q_rec):

    #initialize the send queue
    #
    q_send.put(0)

    #This is the port we will send to on the listening machine
    #this port needs to be 8888 on receiving side
    #
    TCP_PORT = 5005
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to connect to passed IP
    #
    try:
        s.connect((TCP_IP, TCP_PORT))
    except socket.error, exc:
        raise socket.error

    while True:

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

        MESSAGE = input("Enter Message:\n >> ")

        #send the message
        #
        s.send(bytes(MESSAGE, 'UTF-8'))

        #if we get the exit message, close the socket, signal the receive thread and
        #then let the thread terminate
        #
        if(MESSAGE == "EXIT"):
            q_send.put(1)
            s.close()
            break

    # Exit with normal 
    return 0