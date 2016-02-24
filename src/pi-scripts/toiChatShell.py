#!/usr/bin/env python3
# 
# Python toiChat Command Line Interpreter
#
# Created on: 02/09/2016
# Author: Toi-Group
#
from modules.toiChatServer import toiChatServer
from modules.toiChatClient import toiChatClient
from modules.toiChatter import toiChatter
from modules.toiChatNameServer import toiChatNameServer
import cmd, sys, os

class toiChatShell(cmd.Cmd):

    intro = "ToiChat - A Mesh Network optimized communication application."
    prompt = "\ntoiChatShell >> "
    myFile = None

    # ----- basic toiChat commands -----
    def do_startserver(self, arg):
        'Start the toiChat Server'
        if self.myToiChatServer.statusServer() == True:
            print("Server is already running.")
            return
        yesNoReponse = self.askYesNo("Do you want start your server " +\
                "on a non-standard port?")
        if yesNoReponse == None:
            return
        if yesNoReponse == True:
            self.myToiChatServer.startServer(self.askForValidPort())
        self.myToiChatServer.startServer()

    def do_forceupdatedns(self, arg):
        'Connects to local router in a attempt to find other toiChatServers'
        if self.myToiChatServer.statusServer() == False:
            print("We found you are not running a ToiChatServer " + \
            "yet. Please start the toiChatServer before continuing.")
            return
        yesNoReponse = self.askYesNo("Do you want to search for server " +\
                "on a non-standard port?")
        if yesNoReponse == None:
            return
        if yesNoReponse == True:
            self.myNameServer.attemptFindServer(self.askForValidPort())
        if self.myNameServer.attemptFindServer()== True:
            print("Connection to a toiChatNetwork successful.")
            return
        else:
            print("Connection to a toiChatNetwork failed. Please try " + \
                "again in a few minutes.")

    def do_stopserver(self, arg):
        'Stop the toiChat Server'
        if self.myToiChatServer.statusServer() == False:
            print("Server is not running.")
            return
        if self.myToiChatServer.stopServer() == False:
            print("Attempt to stop server failed. Please try again")
            return
        print("Attempt to stop server was successful!")
        return

    def do_statusserver(self, arg):
        'Returns status of the ToiChatServer instance.'
        if self.myToiChatServer.statusServer() == False:
            print("Server is not running.")
        elif self.myToiChatServer.statusServer() == True:
            print("Server is running.")
        return

    def do_printdns(self, arg):
        'Print Current DNS Table'
        self.myNameServer.printDNSTable()

    def do_startchat(self, arg):
        'Start a instant message with another user'
        if self.myToiChatServer.statusServer() == False:
            print("We found you are not running a ToiChatServer " + \
            "yet. Please start the toiChatServer before continuing.")
            return
        if self.myNameServer.lookupDnsLegnth() == 1:
            print("We see your DNS table is empty. Try running '" + \
                "forceupdatedns' to look for other people in the network.")
            return
        print("Available users to Chat: ")
        self.myNameServer.printClients()
        while True:
            try:
                recipient = input("Who do you want to talk to? \n >> ")
            except KeyboardInterrupt:
                return
            if not self.myNameServer.lookupIPByHostname(recipient) == None:
                break
            else:
                print(str(recipient) + " is not a valid name. " + \
                    "Please enter a valid name.")
        self.myToiChatter = toiChatter(self.myToiChatClient, recipient)
        self.myToiChatServer.addToiChatter(self.myToiChatter)
        self.myToiChatter.startInstantMessage()
        self.myToiChatServer.removeToiChatter(self.myToiChatter)
        return

    def do_bye(self, arg):
        'Close the toiChat shell, and exit program.'
        if self.myToiChatServer.statusServer() == True:
            print("Toi-Chat server is running in the " + \
                "background.\n")
        if self.askYesNo("Are you sure you want to quit?") == True:
            if self.myToiChatServer.stopServer() == False:
                print("Attempt to stop server failed. Please try again")
                return
            self.close()
            print('\nThank you for using TOIChat!')
            return
        

    # ----- record and playback -----
    def precmd(self, line):
        line = line.lower()
        if self.myFile and 'playback' not in line:
            print(line, file=self.myFile)
        return line

    def close(self):
        if self.myFile:
            self.myFile.close()
            self.myFile = None

    def start(self):
        while True:
            # Initialize client, server and name-server
            # Prompt user for their unique name input
            #
            while True:
                try:
                    callSign = str(input("What is your host-name " + \
                        "(call sign)?:\n >>  ")).lower()
                except KeyboardInterrupt:
                    self.close()
                    print('\nThank you for using TOIChat!')
                    return True
                if not callSign == "":
                    break
                else:
                    print("Error: You need to enter a call sign.")
            # Prompt user for call sign input
            #
            yesNoReponse = self.askYesNo("Do you want to register any misc " + \
                "information? (optional)")
            if yesNoReponse == None:
                sys.stdout.write("\033[K") # Clear the current line
                print("\n")
                continue
            elif yesNoReponse == True:
                myDesc = str(input("Enter misc information now?:\n >>  "))
                self.myToiChatClient = toiChatClient(callSign, myDesc)
                break
            self.myToiChatClient = toiChatClient(callSign)
            break
        
        self.myNameServer = toiChatNameServer(self.myToiChatClient)
        self.myToiChatClient.updateNameServer(self.myNameServer)
        self.myToiChatServer = toiChatServer(self.myNameServer)

        # Start toiChat shell
        #
        self.cmdloop()

    # ---- Internal ----
    def askYesNo(self, question):
        while True:
            try:
                yesNoQ = input(question + " (yes|no):\n >>  ")
            except KeyboardInterrupt:
                return None
            if str.lower(yesNoQ) == "yes":
                return True
            elif str.lower(yesNoQ) == "no":
                return False
            else:
                print("Please specify yes or no.")

    def askForValidPort(self):
        # Loop until user provides a valid port
        #
        while True:
            try:
                myPort = int(input("What Port do you want to " + \
                    "use? (Default=5005):\n >>  ") or '5005')
            except KeyboardInterrupt:
                return None
            except ValueError:
                print("You need to type in a valid PORT number!")
                continue
            else:
                if myPort in range(65535):
                    return myPort
                else:
                    print("Port must be in range 0-65535!")
                    continue

    # Catch keyboard interrupt
    #
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt as e:
            print("\n")
            # Upon interrupt on main console shut down server and close
            #
            self.myToiChatServer.stopServer()
            sys.exit(0)

if __name__ == '__main__':
    # Check to make sure the program is ran as root
    #
    if not os.geteuid() == 0:
        print("You need to run this program with administrative privileges.")
        sys.exit(0)
    toiChatShell().start()
