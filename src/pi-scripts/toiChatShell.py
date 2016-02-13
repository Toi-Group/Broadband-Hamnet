#!/usr/bin/env python3
# 
# Python toiChat Command Line Interpreter
#
# Created on: 02/09/2016
# Author: Toi-Group
#
from modules.toiChatServer import toiChatServer
from modules.toiChatClient import toiChatClient
from modules.toiChatNameServer import toiChatNameServer
import cmd, sys

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
        if self.askYesNo("Do you want start your server " +\
                "on a non-standard port?"):
            self.myToiChatServer.startServer(askForValidPort())
        self.myToiChatServer.startServer()

    def do_forceupdatedns(self, arg):
        'Connects to local router in a attempt to find other toiChatServers'
        if self.myToiChatServer.statusServer() == False:
            print("We found you are not running a ToiChatServer " + \
            "yet. Please start the toiChatServer before continuing.")
            return
        if self.askYesNo("Do you want to search for server " +\
                "on a non-standard port?"):
            self.myNameServer.attemptFindServer(askForValidPort())
        self.myNameServer.attemptFindServer()

    def do_stopserver(self, arg):
        'Stop the toiChat Server'
        if self.myToiChatServer.stopServer() == False:
            print("Attempt to stop server failed. Please try again")
            return
        return

    def do_statusserver(self, arg):
        if self.myToiChatServer.statusServer() == False:
            print("Server is not running.")
        elif self.myToiChatServer.statusServer() == True:
            print("Server is running.")
        return

    def do_printdns(self, arg):
        'Print Current DNS Table'
        self.myNameServer.printDNSTable()

    def do_bye(self, arg):
        'Stop recording, close the toiChat shell, and exit: BYE'
        if self.myToiChatServer.statusServer() == True:
            if self.askYesNo("Toi-Chat server is running in the " + \
                "background. Are you sure you want to quit?"):
                if self.do_stopserver() == False:
                    return
            else:
                return
        self.close()
        print('Thank you for using toiChat!')
        return True

    # ----- record and playback -----
    def do_record(self, arg):
        'Save future commands to filename:  RECORD myToiChatPref.cmd'
        self.myFile = open(arg, 'w')
    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK myToiChatPref.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())

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
        # Initialize client, server and name-server
        # Prompt user for their unique name input
        #
        callSign = str(input("What is your host-name (call sign)?:\n >>  "))
        
        # Prompt user for call sign input
        #
        myDesc = str("")
        if self.askYesNo("Do you want to register any misc information? (optional)"):
            myDesc = str(input("Enter misc information now?:\n >>  "))

        self.myToiChatClient = toiChatClient(callSign, myDesc)
        self.myNameServer = toiChatNameServer(self.myToiChatClient)
        self.myToiChatClient.updateNameServer(self.myNameServer)
        self.myToiChatServer = toiChatServer(self.myNameServer)

        # Start toiChat shell
        #
        self.cmdloop()

    # ---- Internal ----
    def askYesNo(self, question):
        while True:
            yesNoQ = input(question + " (yes|no):\n >>  ")
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
    toiChatShell().start()
