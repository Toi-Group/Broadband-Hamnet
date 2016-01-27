#!/usr/bin/env python3

import socket
from threading import Thread
import sys
import queue
from modules.receiveTCP import receiveTCP
from modules.sendTCP import sendTCP

#main
#intilizes threads and queues
#
def main():
    localIP = socket.gethostbyname(socket.gethostname())
    
    while True:
        print ("\n Enter the IP of the machine you will be "
            "communicating with.")
        TCP_IP = input(" >> ")
        try:
            socket.inet_aton(TCP_IP)
            # Legal
            break
        except socket.error:
            # Not Legal
            print("You need to enter a valid IPv4 address!\n")
            continue
        
    #instantiate a queue object.  We will use this to share data across 
    #threads
    #
    q_send = queue.Queue()
    q_rec = queue.Queue()

    #start a thread to receive, and a thread to send
    #
    R = Thread(target=receiveTCP, args=(localIP, q_send,q_rec,))
    S = Thread(target=sendTCP, args=(TCP_IP, q_send,q_rec,))
    S.daemon = True
    
    #start the threads
    #
    R.start()
    S.start()

if __name__ == '__main__':
    main()

