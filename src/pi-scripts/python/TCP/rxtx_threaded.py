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

    # Start a Rx thread
    #
    R = Thread(target=receiveTCP, args=(localIP, q_send,q_rec,))
    R.start()
    
    # Get a list of IPs running Toi-Chat software on the mesh network
    #
    try:
        list_IPS = conn_router("10.93.121.49")
    except 

    for TCP_IP in list_IPS:
         try:
            # Start a thread to send data
            #
            S = Thread(target=sendTCP, args=(TCP_IP, q_send,q_rec,))
            S.daemon = True
            
            # Start the Tx thread
            #
            S.start()

            # Did not fail to connect. Connection to client successful
            # Break out of for loop
            #
            break

         except socket.error:
            if TCP_IP == list_IPS[len(list_IPS)]:
                # We tried all IPs in the list and could not connect to 
                # any. Return error to stdout informing the user
                print("Could not connect to '" + TCP_IP + "'.\n" \
                    "Exhausted known list of hosts")
            else:
                print("Could not connect to '" + TCP_IP + "'.\n" \
                    "Trying next IP in list.")
                pass    

if __name__ == '__main__':
    main()

