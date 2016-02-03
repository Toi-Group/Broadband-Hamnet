#!/usr/bin/env python3
# 
# Python toiChat Class:
#   Services: 
#       toiChatServer 
#       toiChatClient 
#
# Created on: 02/01/2016
# Author: Toi-Group
#

import protobuf.ToiChatProtocol
import socket
from threading import Thread
import queue
import struct, sys

# ToiChat Server listener
#
class toiChatServer():

    # String constant to send to queues when they shoudl quit
    #
    CONST_EXIT_QUEUE = "EXITTHREAD"

    # Types of messages to expect
    #
    getType={
        0:ToiChatMessage.DnsMessage,
        1:ToiChatMessage.ServerMessage,
        2:ToiChatMessage.OneToOneMessage
    }

    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling server side communication handling
    #   - Defaults to port = 5005
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xHostname, xIP, xDescription, xPORT_TOICHAT=5005):
        # Define port ToiChat uses to communicate
        #
        self.PORT_TOICHAT = xPORT_TOICHAT;

        # Define this machines ToiChat Instance
        #
        self.myToiChat = ToiChatProtocol.ToiChatClient()
        self.myToiChat.clientName = xHostname
        self.myToiChat.clientId = xIP
        self.myToiChat.description = xDescription

        # Server is by default set to disabled
        #
        self.stopServer = False

        # Create a communication handler thread queue
        #
        self.communicateQueue = queue.Queue()

        # Start the client recv connection handler thread
        #
        self.S = Thread(target=self.__pi_server_toichat__).start()

        # Start the communication handler thread
        #
        C = Thread(target=self.__communicate__)
        C.daemon = True
        C.start()
    
    # -- START CLASS DESTRUCTOR -- 
    #
    # ToiChat class destructor stops background threads upon class delete
    #
    # -- END CLASS DESTRUCTOR -- 
    def __del__(self):
        self.stopServer()
    
    # -- START FUNCTION DESCR --
    #
    # Starts a thread listening on PORT_TOICHAT for incoming socket 
    # clientSockections. 
    #
    # Inputs:
    #  None
    #
    # Outputs:
    #   - A thread running server listen operations running
    #
    # -- END FUNCTION DESCR -- 
    def startServer(self):
        # If break out of loop print we are closing the sever
        #
        print("Attempting to start ToiChat server...")

        # Loop the server listener until stop server is true
        #
        self.stopServer = False

        # Start the server listener thread
        #
        S = Thread(target=self.__pi_server_toichat__)
        S.daemon = True
        S.start()

        # Determine if server listener thread stopped correctly
        #
        if self.S.is_alive() == True:
            print("\tAttempt to start server was successful!\n\n")
        else:
            print("\tAttempt to start server failed.\n\n")
        return 1

    # -- START FUNCTION DESCR --
    #
    # Stop all threads created by startServer
    #
    # Inputs:
    #   - A thread running server listen operations running
    #
    # Outputs:
    #   - A thread running server listen operations stopped
    #
    # -- END FUNCTION DESCR -- 
    def stopServer(self):
        # If break out of loop print we are closing the sever
        #
        print("Attempting to stop ToiChat server...")

        # Tell the server listener thread to break accepting connections
        #
        self.stopServer = True

        # Wait until the listen thread is over
        #
        self.S.join()

        # Determine if server listener thread stopped correctly
        #
        if self.S.is_alive() == True:
            print("\tAttempt to stop server failed.\n\n")
        else:
            print("\tAttempt to stop server was successful!\n\n")
        return 1

    # -- START FUNCTION DESCR --
    #
    # Tries toiServerIP ToiChat Server. May raise an exception if 
    # clientSockection is unsuccessful. 
    #
    # Inputs:
    #  - toiServerIP = ToiChat server to attempt clientSockection to
    #
    # Outputs:
    #   - Returns true if server connection was successful and 
    #       the server successful added
    #
    # -- END FUNCTION DESCR -- 
    def attemptServer(self, toiServerIP, toiServerPORT=self.PORT_TOICHAT):
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket clientSockection timeout
        #
        serverSock.settimeout(10) 

        # Try to clientSockect to passed IP
        #
        serverSock.clientSockect((toiServerIP, toiServerPORT))
        
        # If successful connection, tell the server to register this 
        # machine in it DNS.
        #

        serverSock.close()
        return 1

    # --------------------------------------------------------------------
    # ------------------- START OF PRIVATE FUNCTIONS ---------------------
    # --------------------------------------------------------------------
    # -- START FUNCTION DESCR -- 
    #
    # Open a port on the PI to act as the ToiChat server listener.
    #
    # Inputs:
    #  - PORT_TOICHAT = Port the server should listen on
    #
    # Outputs:
    #  - communicateQueue = output is on the communicateQueue queue that  
    #       contains client sockets waiting to be processed. 
    #
    #
    # -- END FUNCTION DESCR -- 
    def __pi_server_toichat__(self):
        # Create a tuple with listening on localhost and PORT_TOICHAT
        #
        SERVER = ('', self.PORT_TOICHAT)

        # Begin process of accepting incoming clientSockection on 
        # designated port
        #
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSock:
            # Bind to localhost on PORT_TOICHAT 
            #
            serverSock.bind(SERVER)

            # Allow for 5 clients to enter queue
            #
            serverSock.listen(5)

            # Set socket serverSocket timeout to check if we should stop
            # running the server
            #
            serverSock.settimeout(10) 

            while True:
                # Accept incoming client connections
                #
                clientSock, addr = serverSock.accept()

                # Check if we have a valid socket connection to a client
                #
                if clientSock:
                    # When a clientSockection is found put it into the 
                    # processing message queue.
                    #
                    self.communicateQueue.put([clientSock, None])
                
                # Check if we should stop listening 
                #
                if self.stopServer = True:
                    break
        return 1

    # -- START FUNCTION DESCR -- 
    #
    # From socket received message up to MSGLEN. 
    #
    # Inputs:
    #  - clientSock = socket clientSockected a client machine
    #  - MSGLEN = received the message on the socket up to this length.
    #
    # Outputs:
    #  - data_packet = outputs message in binary format.
    #
    #
    # -- END FUNCTION DESCR -- 
    def __recvall__(self, clientSock, MSGLEN):
        # Get the client's IP
        #
        clientIP = clientSock.getpeername()

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
                print("clientSockection to client '" + \
                    str(clientIP) + "' lost.")
                return None

            # Append the data to the overall message
            #
            data += data_packet
        return data_packet


    # -- START FUNCTION DESCR -- 
    #
    # Processes the message with client seen on socket passed
    #
    # Inputs:
    #  - communicateQueue = input is on the communicateQueue that  
    #       messages are put on to either send or receive.
    #
    # Outputs:
    #  - Either sends a message or receive a message that
    #
    # -- END FUNCTION DESCR -- 
    def __communicate__(self):
        while True:
            # Get a client socket clientSockection from server listen 
            # thread
            #
            [clientSock, MSG] = self.communicateQueue.get()

            # Get if queueEXIT STATUS is true. Stop thread if true.
            #
            if MSG == self.CONST_EXIT_QUEUE:
                break
            
            # Check if socket is still open
            #
            if clientSock:
                # Check if MSG is null to determine whether we are 
                # receiving or sending a message to client
                #
                if MSG = None:
                    # Receive the first four bytes containing the length    
                    # of the message
                    #
                    raw_MSGLEN = self.__recvall__(clientSock, 4)

                    # Ensure the length of the message is not empty
                    #
                    if not raw_MSGLEN:
                        clientSock.close()
                        continue

                    # Get the length of the message from the data header
                    #
                    MSGLEN = struct.unpack('>I', raw_MSGLEN)[0]

                    # Output the message sent by the client to message parser 
                    # thread. Also pass the type of message
                    #
                    rawBuffer = self.__recvall__(clientSock, MSGLEN))

                    # Process RAW MESSAGE
                    #
                    self.messageProcess(clientSock, rawBuffer)
                else:
                    # We are sending information back to the client
                    #
                    self.__sendToiMessage__(clientSock, MSG)

            # Client closed connect so we close connection too. 
            #
            clientSock.close()
        return 1


    # -- START FUNCTION DESCR --
    #
    # Sends a ToiChatMessage over a socket by appending the length of the  
    # message to the beginning to ensure the full message is sent. 
    #
    # Inputs:
    #  - clientSock = Client socket we will send message to. 
    #  - MSG = Serialized Message user is trying to send
    #
    # Outputs:
    #   - Returns true if message was sent successfully. 
    #
    # -- END FUNCTION DESCR -- 
    def __sendToiMessage__(self, clientSock, decodedMsg):
        # Convert ToiChatMessage to binary stream.
        # 
        encodedMsg = SerializeToString(decodedMsg)
        
        # Append the length of the message to the beginning
        #
        encodedMsg = struct.pack('>I', len(encodedMsg)) + encodedMsg

        # Put message on communicate queue.
        #
        self.communicateQueue.put([clientSock, encodedMsg])
        return 1
    

    # -- START FUNCTION DESCR --
    #
    # Decodes message based on its type
    #
    # Inputs:
    #   clientSocket = 
    #   rawBuffer = 
    #
    # Outputs:
    # 
    #
    # -- END FUNCTION DESCR --
    def __messageProcess__(self, clientSock, rawBuffer):
        # Create a ToiChat Message Type 
        #
        decodeMsg = ToiChatMessage()

        # Decode the raw message 
        #
        decodeMsg.ParseFromString(rawBuffer)
        
        # Find the type of message sent
        #
        msgType = decodeMsg.WhichOneOf("messageType")

        if msgType == getType[0]:
            handleDnsNewClient(decodeMsg.msgType)
        elif msgType == getType[0]:
            handleRequestDns(decodeMsg.msgType)
        else:
            print("Unknown MsgItem Type.")
        return