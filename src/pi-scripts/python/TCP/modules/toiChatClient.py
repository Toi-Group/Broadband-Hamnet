#!/usr/bin/env python3
# 
# Python toiChat Class:
#   Services: 
#       toiChatserver 
#
# Created on: 02/04/2016
# Author: Toi-Group
#

import protobuf.ToiChatProtocol_pb2
import socket
from io import StringIO
import struct, sys

from modules.conn_router import conn_router
import modules.toiChatServer
from modules.gatewayIP import gatewayIP

class toiChatserver():

    # Types of messages to expect
    #
    getType={
        0:ToiChatMessage.DnsMessage,
        1:ToiChatMessage.ServerMessage,
        2:ToiChatMessage.OneToOneMessage
    }

    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling server side communication
    #   - Defaults to port = 5005
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xHostname, xDescription="", xPORT_TOICHAT=5005):
        # Describe this toichatserver hostname/callsign
        #
        self.serverName = xHostname
        
        # Misc information about this toichatserver
        #
        self.description = xDescription

        # Define port ToiChat uses to communicate
        #
        self.PORT_TOICHAT = xPORT_TOICHAT;

        # Create a toiChatServer instance which we use to create messages
        #
        self.mytoiChatServer = toiChatServer(self.serverName, \
            self.description)

        # Create dns object instance
        #
        # 

    # -- START __FUNCTION DESCR --
    #
    # Decodes message based on its type
    #
    # Inputs:
    #   serverSocket = 
    #   rawBuffer = 
    #
    # Outputs:
    # 
    #
    # -- END FUNCTION DESCR --
    def attemptFindServer(self):
        # Get a list of IPs running Toi-Chat software on the mesh network
        #
        list_IPS = conn_router(gatewayIP())

        # Check to see if there are any IPs in the returned ARP list
        #
        if list_IPS == None:
            return -1

        for toiServerIP in list_IPS:
            # Print to stdout what we are trying to connect to
            #
            print("Trying to connect to '" + toiServerIP + "'...")
            serverMsg = self.mytoiChatServer.createRemoteServerMessage("status")
            try:
                self.__sendToiMessage__(toiServerIP, serverMsg, True)
            except Exception as e:
                if toiServerIP == list_IPS[len(list_IPS)-1]:
                    # We tried all IPs in the list and could not connect to 
                    # any. Return error to stdout informing the user
                    print("Could not connect to '" + toiServerIP + "'.\n" + \
                        "Exited with status: \n\t" + str(e) + "\n" \
                        "Exhausted known list of hosts.\n\n")
                    pass
                    return -1
                else:
                    print("Could not connect to '" + toiServerIP + "'... " + \
                        "Exited with status: \n\t" + str(e) + "\n" \
                        "Trying next IP in list.")
                    continue 
            # Did not fail to connect. Connection to server successful
            # Break out of for loop
            #

            print("Connection to a server successful.")
            return 1
    # -- START FUNCTION DESCR -- 
    #
    # Processes the message with server seen on socket passed
    #
    # Inputs:
    #  - communicateQueue = input is on the communicateQueue that  
    #       messages are put on to either send or receive.
    #
    # Outputs:
    #  - Either sends a message or receive a message that
    #
    # -- END FUNCTION DESCR -- 
    def sendMessage(self, serverSock, MSG):       
        # Check if socket is still open
        #
        if serverSock:
            # Check if MSG is null to determine whether we are 
            # receiving or sending a message to server
            #
            if MSG == None:
                # Print that we have a new connection
                #
                serverIP = serverSock.getpeername()

                print("Connected to - '" + str(serverIP) + "'")
                # Receive the first four bytes containing the length    
                # of the message
                #
                raw_MSGLEN = self.__recvall__(serverSock, 4)

                # Ensure the length of the message is not empty
                #
                if not raw_MSGLEN:
                    serverSock.close()
                    continue

                # Get the length of the message from the data header
                #
                MSGLEN = struct.unpack('>I', raw_MSGLEN)[0]

                # Output the message sent by the server to message parser 
                # thread. Also pass the type of message
                #
                rawBuffer = self.__recvall__(serverSock, MSGLEN)

                # Process RAW MESSAGE
                #
                self.__messageProcess__(serverSock, rawBuffer)
                return 1
            else:
                # We are sending information back to the server
                #
                return self.__sendToiMessage__(serverSock, MSG)

        # server closed connect so we close connection too. 
        #
        print("\tDisconnected from - '" + str(serverIP) + "'")
        serverSock.close()
        return 1

    # --------------------------------------------------------------------
    # ------------------- START OF PRIVATE FUNCTIONS ---------------------
    # --------------------------------------------------------------------
    # -- START __FUNCTION DESCR --
    #
    # Decodes message based on its type
    #
    # Inputs:
    #   serverSocket = 
    #   rawBuffer = 
    #
    # Outputs:
    # 
    #
    # -- END FUNCTION DESCR --
    def __messageProcess__(self, serverSock, rawBuffer):
        # Create a ToiChat Message Type 
        #
        decodedToiMessage = ToiChatMessage()

        # Decode the raw message 
        #
        decodedToiMessage.ParseFromString(rawBuffer)
        
        # Find the type of message sent
        #
        msgType = decodedToiMessage.WhichOneOf("messageType")

        if msgType == self.getType[0]:
            decodeDnsMsg = DnsMessage()
            decodeDnsMsg.ParseFromString(decodedToiMessage)
            handleDnsMessage(serverSock, decodeDnsMsg)
        elif msgType == self.getType[1]:
            decodeServerMsg = ServerMessage()
            decodeServerMsg.ParseFromString(decodedToiMessage)
            self.__handleServerMessage__(serverSock, decodeServerMsg)
        else:
            print("Unknown MsgItem Type.")
        return

        # -- START FUNCTION DESCR --
    #
    # Sends a ToiChatMessage over a to a ToiChatSeve. This function will 
    # append the length of the message to the beginning to 
    # ensure the full message is sent. 
    #
    # Inputs:
    #  - toiServerIP = ToiChat server you wish to connect to
    #  - rawMsg = message type as defined by ToiChatMessage Protocol
    #  - outPut = Whether the message you are sending expects an output
    #
    # Outputs:
    #   - Returns true if message was sent successfully. 
    #
    # -- END FUNCTION DESCR -- 
    def __sendToiMessage__(self, toiServerIP, rawMsg, outPut):
        # Else do a DNS lookup
        #
        #toiServerIP = dnsGetIP(toiServerHostnameorIP)

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

        # Create a new ToiChatMessage object
        #
        decodedToiMessage = ToiChatMessage()

        # Input the message into the ToiChatMessage
        #
        decodedToiMessage.msgType = rawMsg

        # Convert ToiChatMessage to binary stream.
        # 
        encodedToiMessage = decodedToiMessage.SerializeToString()
        
        # Append the length of the message to the beginning
        #
        encodedToiMessage = struct.pack('>I', len(encodedToiMessage)) + \
            encodedToiMessage

        # Send message over socket
        #
        self.sendMessage(serverSock, encodedToiMessage)

        if outPut = True:
            # If we expect an output we wait for server response
            #
            self.__messageProcess__(serverSock, encodedToiMessage)
        return 1




    # -- START FUNCTION DESCR -- 
    #
    # From socket received message up to MSGLEN. 
    #
    # Inputs:
    #  - serverSock = socket serverSockected a server machine
    #  - MSGLEN = received the message on the socket up to this length.
    #
    # Outputs:
    #  - data_packet = outputs message in binary format.
    #
    #
    # -- END FUNCTION DESCR -- 
    def __recvall__(self, serverSock, MSGLEN):
        # Get the server's IP
        #
        serverIP = serverSock.getpeername()

        # Initiate an array with the message being sent by server
        #
        data = b''
        
        # While the server is still sending a message
        #
        while len(data) < MSGLEN:
            # Keep reading message from server
            #
            data_packet = serverSock.recv(MSGLEN - len(data))
            if not data_packet:
                print("\tConnection to '" + \
                    str(serverIP) + "' lost.")
                return None

            # Append the data to the overall message
            #
            data += data_packet
        return data_packet

