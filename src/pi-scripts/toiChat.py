#!/usr/bin/env python3

# 
# Python toiChat Front-End Runner
#   Script that interacts with background services such as toiChatServer 
#   toiChatClient and application services such as toiChatNameServer. 
#
#
# Created on: 02/07/2016
# Author: Toi-Group
#
import argparse, sys
from modules.toiChatServer import toiChatServer
from modules.toiChatClient import toiChatClient
from modules.toiChatNameServer import toiChatNameServer

# Front-end ToiChat runner main program start
#
def main():
    # Create a list of possible input arguments
    #
    parser = argparse.ArgumentParser(prog="toiChat.py", \
        description="ToiChat - A Mesh Network " + \
        "optimized communication application.")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("--exit", action="store_true", \
        help="Exit the program")
    group.add_argument("-s", "--start", choices=["server", "client"], \
        default="", help='Start ToiChat Service')
    group.add_argument("-e", "--stop", choices=["server", "client"], \
        default="", help='Stop a ToiChat Service')
    parser.add_argument("-l", "--list", action="store_true", \
        help="List available ToiChat Services")
    parser.add_argument("-d", "--dns", action="store_true", \
        help="Print the current DNS Table")

    # Prompt user for their unique name input
    #
    callSign = str(input("What is your call sign?:\n >>  "))
    
    # Prompt user for call sign input
    #
    myDesc = str("")
    if askYesNo("Do you want to register any misc information? (optional)"):
        myDesc = str(input("Enter misc information now?:\n >>  "))

    # Create a service instances
    #
    myToiChatClient = toiChatClient(callSign, myDesc)
    myNameServer = toiChatNameServer(myToiChatClient)
    myToiChatClient.updateNameServer(myNameServer)
    myToiChatServer = toiChatServer(myNameServer)
    
    while True:
        # Check if user passed any arguments upon program start
        #
        if len(sys.argv) > 1:
            # Copy inputed arguments into variable
            #
            cmdInput = ''.join(sys.argv[1:])
            # Clear arguments imported on system startup for it does not 
            # interfere with next loop iteration
            #
            del sys.argv[1:]

        # If no arguments were passed prompt user for input
        #
        else:
            # Program started with no input. Print usage for use
            #
            parser.print_help()

            # Prompt user for input
            #
            cmdInput = input(">> ")

        # Parsed user inputed parameters. Ignore if passed unknown flags
        #
        args, unknownArgs = parser.parse_known_args(cmdInput.split())
        print(args)
        # Parse the user input for commands
        #
        # Check to see if user wants to print the current DNS table
        #
        if args.dns == True:
            myNameServer.printDNSTable()

        # Check to see if user wants to start a ToiChat Server
        #
        if args.start == "server":
            if askYesNo("Do you want start your server " +\
                "on a non-standard port?"):
                myToiChatServer.startServer(askForValidPort())
            else:
                myToiChatServer.startServer()
        elif args.start == "client":
            # Prompt user for port usage
            #
            if askYesNo("Do you want to search for server " +\
                "on a non-standard port?"):
                myToiChatClient.attemptFindServer(askForValidPort())
            else:
                myToiChatClient.attemptFindServer()
                
        # Check if user wants to stop a service
        #
        if args.stop == "server":
            myToiChatServer.stopServer()

        # Inform user there are some unknown flags. Print correct usage
        # for user
        #
        if len(unknownArgs):
            print("\nIgnored unrecognized flags - " + str(unknownArgs) + \
                ". Please see correct usage:")
            parser.print_help()
            pass
            continue
        
        # Check if we should exit the program
        #
        if args.exit == True:
            if myToiChatServer.statusServer:
                if not askYesNo("Toi-Chat server is running in the " + \
                    "background. Are you sure you want to quit?"):
                    continue
            break

def askYesNo(question):
    while True:
        yesNoQ = input(question + " (yes|no):\n >>  ")
        if str.lower(yesNoQ) == "yes":
            return True
        elif str.lower(yesNoQ) == "no":
            return False
        else:
            print("Please specify yes or no.")

def askForValidPort():
    # Loop until user provides a valid port
    #
    while True:
        try:
            myPort = int(input("What Port do you want to " + \
                "use? (Default=5005):\n >>  ") or '5005')
        except ValueError:
            print("You need to type in a valid PORT number!")
            continue
        else:
            if myPort in range(65535):
                return myPort
            else:
                print("Port must be in range 0-65535!")
                continue


if __name__ == '__main__':
    main()