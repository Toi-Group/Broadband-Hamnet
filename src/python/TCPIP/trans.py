#!/usr/bin/env python

import socket
from threading import Thread
import sys
import Queue


def receiveTCP(q_send,q_rec):

    #initializ the receive queue
    q_rec.put(0)

    TCP_IP = raw_input('Enter IPv4 of this Machine: ')

    #port this machine listens on
    #this needs to be the send port of other machine
    #
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    
    #create a tuple with port and ip
    DEST = (TCP_IP, TCP_PORT)


    #begin process of accepting incoming connection on designated port
    #
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((DEST))
    s.listen(1)
    conn, addr = s.accept()
   
    #prints who we are connected to
    #
    print 'Connection address:', addr

    #wait for messages
    while 1:

        #first we check if the send queue is empty
        if q_send.empty():
            #if the send q is empty, put a 0 on it.
            q_send.put(0)

        #check what is on the send queue.  If it is 1, break from the 
        #while loop which terminates the thread. We also have to close the socket
        check = q_send.get()
        if check:
            conn.close()
            break

        data = conn.recv(BUFFER_SIZE)
        print "received data:", data
        #if we received EXIT from the other machine, signal the 
        #sending thread to terminate and break from the while loop
        #which closes the program
        #
        if data == 'EXIT':
            conn.close()
            s.close()
            q_rec.put(1)
            break
        else:
            q_rec.put(0)


#        conn.send(data)  # echo
    print "closing send thread"

def sendTCP(q_send,q_rec):

    #initialize the send queue
    q_send.put(0)

    TCP_IP = raw_input('Enter IPv4 address of Recipient: ')
    #This is the port we will send to on the listening machine
    #this port needs to be 8888 on receiving side
    TCP_PORT = 8888
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    while 1:

        #Ensure the rec queue is not empty
        if q_rec.empty():
            #if it is empty, put a 0 on the queue
            q_rec.put(0)

        #check the receive thread's status
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
        else:
            q_send.put(0)
            
        #listen for confirmation
        #response = s.recv(BUFFER_SIZE)
        #if response != None:
        #    print "%s received message: %s" % (TCP_IP, response)
        



def main():

    #instantiate a queue object.  We will use this to share data across 
    #threads
    #
    q_send = Queue.Queue()
    q_rec = Queue.Queue()

    #start a thread to receive, and a thread to send
    #
    R = Thread(target=receiveTCP, args=(q_send,q_rec,))
    S = Thread(target=sendTCP, args=(q_send,q_rec,))

    #start the threads
    #
    R.start()
    S.start()
    
if __name__ == '__main__':
    main()

