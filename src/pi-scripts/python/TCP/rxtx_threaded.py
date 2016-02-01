#!/usr/bin/env python3

import socket
from threading import Thread
import sys
import queue
from modules.receiveTCP import receiveTCP
from modules.sendTCP import sendTCP
from modules.conn_router import conn_router

# main program
#
def main():
    
    # Get local IP Address
    #
    localIP = socket.gethostbyname(socket.gethostname())
    
    q_send = queue.Queue()
    q_rec = queue.Queue()

    #start a thread to receive
    #
    R = Thread(target=receiveTCP, args=(localIP, q_send,q_rec,))
    R.start()
 
    TCP_IP = conn_router("10.93.121.49")
    print(TCP_IP) 
    # start a thread to send data
    #
    while True:
         try:
             socket.inet_aton(TCP_IP[0])
             # Legal
             break
         except socket.error:
    #         # Not Legal
              print("You need to enter a valid IPv4 address!\n")
              continue
    
    TCP_IP = conn_router("10.93.121.49")   

    # Separate list of IPs by space
    #
    list_IPS = TCP_IP.split()
    print(list_IPS)
    #instantiate a queue object.  We will use this to share data across 
    #threads
    #
    S = Thread(target=sendTCP, args=(list_IPS[0], q_send,q_rec,))
    S.daemon = True
    
    #start the threads
    #
    
    S.start()

if __name__ == '__main__':
    main()

