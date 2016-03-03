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
import logging

# toiChatClient sends messages to a toiChatServer in network
#
class toiChatClient():

    # Types of messages to expect as defined in ToiChatProtocol
    #
    getType={
        0:"dnsMessage",
        1:"chatMessage"
    }
    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling client side communication
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xHostname, xDescription="", xtoiChatNameServer=None):
        # Logging instance where should we save client logs to
        #
        self.logger = logging.getLogger(__name__)

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

        # Log successful send message event
        #
        self.logger.info("Message sent to ('" + str(toiServerIP) + \
            "', " + str(toiServerPORT) + ").")
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

    # Create a message populating the headers of the DnsMessage type
    # with this client information.
    #
    def createTemplateIdentifierMessage(self, messageType):
        # Create new ToiChatMessage
        #
        myMessage = ToiChatProtocol_pb2.ToiChatMessage()

        # Get the client name
        #
        myName = self.getName()
        
        # Create message based on type and fill myMessage message with 
        # my information
        #
        if messageType == self.getType[0]:
            # Fill myMessage message with my information
            #
            myMessage.dnsMessage.id.clientName = myName
            myMessage.dnsMessage.id.clientId = \
                self.myToiChatNameServer.lookupIPByHostname(myName)
            myMessage.dnsMessage.id.dateAdded = \
                self.myToiChatNameServer.lookupAddedByHostname(myName)
            myMessage.dnsMessage.id.description = \
                self.myToiChatNameServer.lookupDescByHostname(myName)
        elif messageType == self.getType[1]:
            myMessage.chatMessage.id.clientName = myName
            myMessage.chatMessage.id.clientId = \
                self.myToiChatNameServer.lookupIPByHostname(myName)
            myMessage.chatMessage.id.dateAdded = \
                self.myToiChatNameServer.lookupAddedByHostname(myName)
            myMessage.chatMessage.id.description = \
                self.myToiChatNameServer.lookupDescByHostname(myName)
        else:
            return None
        return myMessage