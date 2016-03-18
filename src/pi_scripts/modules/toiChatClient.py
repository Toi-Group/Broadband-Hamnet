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
    # Sends a ToiChatMessage over the designated socket. Since a
    # socket is passed this function assumes the message being sent
    # is an ACK message so it does not close the passed socket. This function  
    # will append the length of the message to the beginning to 
    # ensure the full message is sent over the socket.
    #
    # Inputs:
    #  - clientSock = Open socket to send message to.
    #  - decodedToiMessage = message type as defined by ToiChatMessage Protocol
    #
    # Outputs:
    #   - Returns true if message was sent successfully.
    #   - Returns the received message if waitRespone=True
    #
    # -- END FUNCTION DESCR -- 
    def sendMessageSocket(self, serverSock, decodedToiMessage, \
        waitResponse=False):        
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

        # Log successful send message event
        #
        self.logger.info("Message sent.")

        if waitResponse==True:
            # REDUDANT CODE FROM: toiChatServer
            # Receive the first four bytes containing the length    
            # of the message
            #
            raw_MSGLEN = self.__recvall__(serverSock, addr, 4)

            # Ensure the length of the message is not empty
            #
            if not raw_MSGLEN:
                serverSock.close()
                return 1

            # Get the length of the message from the data header
            #
            MSGLEN = struct.unpack('>I', raw_MSGLEN)[0]
            self.logger.debug("expected len message = " + str(MSGLEN))
            
            # Continue receiving the full message expected from client
            #
            rawBuffer = self.__recvall__(serverSock, addr, MSGLEN)
            self.logger.debug("actual len message = " + \
                str(len(rawBuffer)))`

            # Create a ToiChat Message Type 
            #
            decodedToiMessage = ToiChatProtocol_pb2.ToiChatMessage()

            self.logger.debug("RAW Received MSG = " + str(rawBuffer))
            # Decode the raw message 
            #
            decodedToiMessage.ParseFromString(rawBuffer)

            # Find the type of message sent
            #
            msgType = decodedToiMessage.WhichOneof("messageType")

            if msgType == self.getType[0]:
                decodeDnsMsg = ToiChatProtocol_pb2.DnsMessage()
                decodeDnsMsg = decodedToiMessage.dnsMessage
                self.logger.debug("Decoded Received MSG = " + \
                    str(decodeDnsMsg))
                return decodeDnsMsg
            else:
                self.logger.error("Unable to Process Message of type. '" \
                    + msgType + "'")
                return 0
        return 1

    # -- START FUNCTION DESCR -- 
    # REDUDANT FUNCTION CODE FROM: toiChatServer
    #
    # From socket passed, receive the message sent by a client up to MSGLEN
    #
    # Inputs:
    #  - clientSock = socket to a toiChatClient
    #  - MSGLEN = received the message on the socket up to this length.
    #
    # Outputs:
    #  - data_packet = outputs message in binary format.
    #
    # -- END FUNCTION DESCR -- 
    def __recvall__(self, clientSock, addr, MSGLEN):
        # Initiate an array with the message being sent by client
        #
        data = b''
        
        # While the client is still sending a message
        #
        while len(data) < MSGLEN:
            # Keep reading message from client
            #
            data_packet = clientSock.recv(MSGLEN - len(data))
            if not data_packet:
                self.logger.info("Connection to '" + \
                    str(addr) + "' lost.")
                return 0

            # Append the data to the overall message
            #
            data += data_packet
        # Return the full message received
        #
        return data

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
        toiServerPORT=5005, waitResponse=False):        
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
        # Log successful send message event
        #
        self.logger.info("Connection to ('" + str(toiServerIP) + \
            "', " + str(toiServerPORT) + ") established.")

        # Send over socket
        #
        response = self.sendMessageSocket(clientSock, decodedToiMessage, \
            waitResponse)

        # Close socket to server
        #
        serverSock.close()

        return response

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
        toiServerPORT=5005, waitResponse=False):
        return self.sendMessage(\
            self.myToiChatNameServer.lookupIPByHostname(toiServerHostname),
            decodedToiMessage, toiServerPORT, waitResponse)

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