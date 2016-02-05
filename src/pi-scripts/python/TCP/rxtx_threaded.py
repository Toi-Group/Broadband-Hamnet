#!/usr/bin/env python3
import sys, time
import modules.toiChatServer
import modules.toiChatClient

# main program
#
def main():   
    # Start the toi-chat server
    #
    myToiChatServer = toiChatServer("KC3GIH")
    myToiChatServer.startServer()

    myToiChatClient == toiChatClient("KC3GIH") 

    while True:
        MESSAGE = input("Do you want to attempt to " + \
            "find other clients? (yes|no):\n >> ")
        if str.lower(MESSAGE) == "yes":
            rtrn = myToiChatClient.attemptFind()
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
    myToiChatServer.stopServer()
    print("Shutting successful. \n\n Goodbye.")
    return 0

if __name__ == '__main__':
    main()

