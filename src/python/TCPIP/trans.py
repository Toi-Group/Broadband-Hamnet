#!/usr/bin/env python

import socket
from threading import Thread
import sys
import Queue
from getMessage import getMessage
from receiveTCP import receiveTCP
from sendTCP import sendTCP

#main
#intilizes threads and queues
#
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
    S.daemon = True
    
    #start the threads
    #
    R.start()
    S.start()

if __name__ == '__main__':
    main()

