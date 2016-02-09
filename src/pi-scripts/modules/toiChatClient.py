#!/usr/bin/env python3
# 
# Python toiChat Class:
#   Services: 
#       toiChatserver 
#
# Created on: 02/04/2016
# Author: Toi-Group
#

from modules.protobuf import ToiChatProtocol_pb2 # Used for encoding 
                                                 # ToiChatMessage 
import socket # Used for sending information to a server
import struct, sys # Used to append the length of a message to the beginning
                   # of the message
from modules.conn_router import conn_router # Used for sending a request
                                            # mesh network lan info to 
                                            # local broadband hamnet router
from modules.gatewayIP import gatewayIP # Used for finding the address
                                        # of the local broadband hamnet
                                        # router

# toiChatClient sends messages to a toiChatServer in network
#
class toiChatClient():
    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling client side communication
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xHostname, xDescription="", xtoiChatNameServer=None):
        # Populate the client information
        #
        self.myName = xHostname
        self.myDescription = xDescription

        # Store ToiChatNameServer to use
        #
        self.myToiChatNameServer = xtoiChatNameServer

    # -- START FUNCTION DESCR --
    #
    # Update Name-server Instance
    #
    # Inputs:
    #   A Name Server Instance
    #
    # Outputs:
    #   Updated internal name-server instance variable
    #
    # -- END FUNCTION DESCR --
    def updateNameServer(self, xtoiChatNameServer):
        self.myToiChatNameServer = xtoiChatNameServer
        return 1

    # -- START FUNCTION DESCR --
    #
    # Return this client's associated description
    #
    # Inputs:
    #   None
    #
    # Outputs:
    #   self.myDescription
    #
    # -- END FUNCTION DESCR --
    def getDescription(self):
        return self.myDescription

    # -- START FUNCTION DESCR --
    #
    # Return this clients communication name
    #
    # Inputs:
    #   None
    #
    # Outputs:
    #   self.myName
    #
    # -- END FUNCTION DESCR --
    def getName(self):
        return self.myName

    # -- START FUNCTION DESCR --
    #
    # Updates this client communication name
    #
    # Inputs:
    #   - New client name
    #
    # Outputs:
    #   - Updates name-server instance with the new name and updates this 
    #       toiChatClient with the new name
    #
    # -- END FUNCTION DESCR --
    def updateName(self, newName):
        oldName = self.myName
        self.myName = newName
        return self.myToiChatNameServer.updateMyName(oldName, self.myName)

    # -- START FUNCTION DESCR --
    #
    # Message locates the local Broadband Hamnet router and will
    # send a command asking it to find all attached devices in the 
    # mesh network. It will then attempt to contact each device in the
    # network to see if any are running an instance of toiChatServer
    #
    # Inputs:
    #   - toiServerPort = The port which we will attempt to contact other
    #       toiChatServers.
    #
    # Outputs:
    #   - Upon successful connection to another toiChatServer we will update
    #       our current DNS table with its
    #   - Upon failure to find another toiChatServer we will return an error
    #
    # -- END FUNCTION DESCR --
    def attemptFindServer(self, toiServerPORT=5005):
        # Get a list of IPs running Toi-Chat software on the mesh network
        #
        list_IPS = conn_router(gatewayIP())

        # Check to see if there are any IPs in the returned ARP list
        #
        if list_IPS == None:
            return 0

        # Create a request DNS information request message
        #
        requestDNS = self.myToiChatNameServer.createRequestDnsMessage()

        for toiServerIP in list_IPS:
            # Print to stdout what we are trying to connect to
            #
            print("Trying to connect to '" + toiServerIP + "'...")
            try:
                self.sendMessage(toiServerIP, requestDNS, toiServerPORT)
            except Exception as e:
                if toiServerIP == list_IPS[len(list_IPS)-1]:
                    # We tried all IPs in the list and could not connect to 
                    # any. Return error to stdout informing the user
                    print("Could not connect to '" + toiServerIP + "'.\n" + \
                        "Exited with status: \n\t" + str(e) + "\n" \
                        "Exhausted known list of hosts.\n\n")
                    return 0
                else:
                    print("Could not connect to '" + toiServerIP + "'... " + \
                        "Exited with status: \n\t" + str(e) + "\n" \
                        "Trying next IP in list.")
                    continue 
            # Did not fail to connect. Connection to server successful
            # Break out of for loop
            #
            break

        print("Connection to a toiChatNetwork successful.")
        return 1

    
    # -- START FUNCTION DESCR --
    #
    # Sends a ToiChatMessage over a to a ToiChatSever. This function will 
    # append the length of the message to the beginning to 
    # ensure the full message is sent over the socket.
    #
    # Inputs:
    #  - toiServerIP = ToiChat server you wish to connect to
    #  - decodedToiMessage = message type as defined by ToiChatMessage Protocol
    #  - toiServerPort = The port which we will attempt to contact other
    #       toiChatServers.
    #
    # Outputs:
    #   - Returns true if message was sent successfully.
    #
    # -- END FUNCTION DESCR -- 
    def sendMessage(self, toiServerIP, decodedToiMessage, \
        toiServerPORT=5005):
        # Create a new socket to the server
        #
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket serverSockection timeout. If server doesn't respond
        # if five seconds say the server can not be contacted. 
        #
        serverSock.settimeout(5.0) 

        # Try to connect to passed IP
        #
        serverSock.connect((toiServerIP, toiServerPORT))
        #
        # Assume connection successful after this point

        # Convert ToiChatMessage to binary stream.
        # 
        encodedToiMessage = decodedToiMessage.SerializeToString()

        # Append the length of the message to the beginning
        #
        encodedToiMessage = struct.pack('>I', len(encodedToiMessage)) + \
            encodedToiMessage

        # Send message over socket
        #
        serverSock.sendall(encodedToiMessage)

        # Close socket to server
        #
        serverSock.close()
        return 1

    # -- START FUNCTION DESCR --
    #
    # Sends a ToiChatMessage over a to a ToiChatSever. This function will
    # call the default sendMessage function with the exception being it
    # first does a name-server lookup
    #
    # Inputs:
    #  - toiServerHostname = ToiChat server you wish to connect to (by name)
    #  - decodedToiMessage = message type as defined by ToiChatMessage Protocol
    #  - toiServerPort = The port which we will attempt to contact other
    #       toiChatServers.
    #
    # Outputs:
    #   - Returns true if message was sent successfully. 
    #
    # -- END FUNCTION DESCR -- 
    def sendMessageByHostname(self, toiServerHostname, decodedToiMessage, \
        toiServerPORT=5005):
        return self.sendMessage(\
            self.myToiChatNameServer.lookupIPByHostname(toiServerHostname),
            decodedToiMessage, toiServerPORT)