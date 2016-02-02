#!/usr/bin/env python3
import sys, time
from modules.conn_router import conn_router
from modules.networking_toichat import networking_toichat
from modules.gatewayIP import gatewayIP

# main program
#
def main():   
    # Start the toi-chat server
    #
    myToiChat = networking_toichat()
    myToiChat.startServer()

    while True:
        MESSAGE = input("Do you want to attempt to " + \
            "find other clients? (yes|no):\n >> ")
        if str.lower(MESSAGE) == "yes":
            rtrn = attemptFind(myToiChat)
            if rtrn == False:
                MESSAGE = print("The application failed to find a " + \
                    "valid ToiChat runner.")
        elif str.lower(MESSAGE) == "no":
            break
        else:
            print("Please specify yes or no.")

    while True:
        MESSAGE = input("Toi-Chat server is running in the " + \
             "background. Spell 'shutdown' when you are done running " + \
             "the program. (shutdown):\n >> ")
        if str.lower(MESSAGE) == "shutdown":
            break
        else:
            print("Please specify 'shutdown'.")

    # Exit Main program runner.
    print("Shutting down application...")
    myToiChat.stopServer()
    print("Shutting successful. \n\n Goodbye.")
    return 0

def attemptFind(myToiChat):
    # Get a list of IPs running Toi-Chat software on the mesh network
    #
    list_IPS = conn_router(gatewayIP())

    # Check to see if there are any IPs in the returned ARP list
    #
    if list_IPS == None:
        return False

    for TCP_IP in list_IPS:
        # Print to stdout what we are trying to connect to
        #
        print("Trying to connect to '" + TCP_IP + "'...")
        
        try:
            myToiChat.attemptToiChatConn(TCP_IP)
        except Exception as e:
            if TCP_IP == list_IPS[len(list_IPS)-1]:
                # We tried all IPs in the list and could not connect to 
                # any. Return error to stdout informing the user
                print("Could not connect to '" + TCP_IP + "'.\n" + \
                    "Exited with status: \n\t" + str(e) + "\n" \
                    "Exhausted known list of hosts.\n\n")
                pass
                return False
            else:
                print("Could not connect to '" + TCP_IP + "'... " + \
                    "Exited with status: \n\t" + str(e) + "\n" \
                    "Trying next IP in list.")
                continue 
        # Did not fail to connect. Connection to client successful
        # Break out of for loop
        #
        print("Connection to a client successful.")
        return True

if __name__ == '__main__':
    main()

