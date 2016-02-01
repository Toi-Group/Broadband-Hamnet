#!/usr/bin/env python3

import socket
from threading import Thread
import sys, time
import queue
from modules.receiveTCP import receiveTCP
from modules.sendTCP import sendTCP
from modules.conn_router import conn_router
from modules.gatewayIP import gatewayIP

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
    while True:
        list_IPS = conn_router(gatewayIP())

        # Check to see if there are any IPs in the returned ARP list
        #
        if list_IPS == None:
            # List of IPS is empty so we wait five seconds and try again
            #
            time.sleep(5)
            continue

        # list_IPS is not empty so break out of loop
        #
        break

    for TCP_IP in list_IPS:
        print("Trying to connect to '" + TCP_IP + "'...")
        # Start a thread to send data
        #
        S = Thread(target=sendTCP, args=(TCP_IP, q_send,q_rec,))
        S.daemon = True
        # Start the Tx thread
        #
        S.start()
        
        # Monitor to see if threw execption
        #
        kind = q_send.get(block=True)

        # Check if what is on queue is an error.
        #
        if kind != None:
            if TCP_IP == list_IPS[len(list_IPS)-1]:
                # We tried all IPs in the list and could not connect to 
                # any. Return error to stdout informing the user
                print("Could not connect to '" + TCP_IP + "'."\
                    #"Exited with status: \n" + kind + "\n" \
                    "Exhausted known list of hosts")
                pass
            else:
                print("Could not connect to '" + TCP_IP + "'."\
                    #"Exited with status: \n" + kind + "\n" \
                    "Trying next IP in list.")
                continue

        # Did not fail to connect. Connection to client successful
        # Break out of for loop
        #
        print("breaking")
        break
    print("Shutting down application")
    q_rec.put(1)

if __name__ == '__main__':
    main()

