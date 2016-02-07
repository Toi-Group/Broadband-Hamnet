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

from modules.protobuf import ToiChatProtocol_pb2
import socket
from threading import Thread
import queue
import struct, sys

# ToiChat Server listener
#
class toiChatServer():

    # String constant to send to queues when they should quit
    #
    CONST_EXIT_QUEUE = "EXITTHREAD"

    # Types of messages to expect
    #
    getType={
        0:"dnsMessage",
        1:"chatMessage"
    }
    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling server side communication 
    #   - Defaults to port = 5005
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xPORT_TOICHAT=5005):
        # Define port ToiChat uses to communicate
        #
        self.PORT_TOICHAT = xPORT_TOICHAT;

        # Server is by default set to disabled
        #
        self.stopServerVar = False

        # Create a communication handler thread queue
        #
        self.communicateQueue = queue.Queue()

        # Create a print to file queue
        #
        self.printQueue = queue.Queue()

        # Start the client recv connection handler thread
        #
        self.S = Thread(target=self.__pi_server_toichat__)

        # Start the communication handler thread
        #
        self.C = Thread(target=self.__communicate__)
        self.C.daemon = True

        # Print server output to file thread
        #
        self.W = Thread(target=self.__printToFile__)
        self.W.daemon = True
        self.W.start()

    
    # -- START CLASS DESTRUCTOR -- 
    #
    # ToiChat class destructor stops background threads upon class delete
    #
    # -- END CLASS DESTRUCTOR -- 
    def __del__(self):
        self.stopServer()
        self.printQueue.put(self.CONST_EXIT_THREAD)
    
    # -- START FUNCTION DESCR --
    #
    # Starts a thread listening on PORT_TOICHAT for incoming socket 
    # clientSockections. 
    #
    # Inputs:
    #  None
    #
    # Outputs:
    #   - A thread running server listen serverMsg.operations running
    #
    # -- END FUNCTION DESCR -- 
    def startServer(self):
        # Check to see if printer thread has already started
        #
        if (self.W.is_alive() == False):
            try:
                self.W.start()
            except RuntimeError as e:
                raise Exception("ERROR: ToiChat server printer thread " + \
                    "failed to start!")
                return 0

        self.printQueue.put("Attempting to start ToiChat server...")

        # Check to see if server listener thread has already started
        #
        if (self.S.is_alive() == False):
            self.stopServerVar = False
            # Attempt to start the server listener
            #
            try:
                self.S.start()
            except RuntimeError as e:
                self.printQueue.put("\tAttempt to start server failed.\n\n")
                return 0
        # Check to see if message processor thread has already started
        #
        if (self.C.is_alive() == False):
            try:
                # Attempt to start the message processor thread
                #
                self.C.start()
            except RuntimeError as e:
                self.printQueue.put("\tAttempt to start server failed.\n\n")
                return 0
        # Both server dependencies are already started
        #
        else:
            self.printQueue.put("\tServer already started.\n\n")
            return 1
        # Server dependencies started successfully.
        #
        self.printQueue.put("\tAttempt to start server was successful!\n\n")
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
        # If break out of loop print we are closing the server
        #
        self.printQueue.put("Attempting to stop ToiChat server...")

        # Tell the server listener thread to break accepting connections
        #
        self.stopServerVar = True

        # Stop the communicateQueue thread handler 
        # 
        self.communicateQueue.put([None, self.CONST_EXIT_QUEUE])
        
        # Wait for both server threads to close
        #
        if (self.S.is_alive() == True):
            self.S.join(3.0)
        if (self.C.is_alive() == True):
            self.C.join(3.0)

        # Determine if server listener thread stopped correctly
        #
        if (self.S.is_alive() or self.C.is_alive()) == True:
            self.printQueue.put("\tAttempt to stop server failed.\n\n")
            return 0
        else:
            self.printQueue.put("\tAttempt to stop server was successful!\n\n")
        return 1

    # -- START FUNCTION DESCR --
    #
    # Returns the server status.
    #
    # Inputs:
    #   None
    #
    # Outputs:
    #   - Returns true if server is running else false.
    #
    # -- END FUNCTION DESCR -- 
    def statusServer(self):
        if (self.S.is_alive() and self.S.is_alive()) == True:
            return 1
        else:
            return 0

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
            # running the server every 2 seconds.
            #
            #serverSock.settimeout(2) 

            while True:
                # Accept incoming client connections
                #
                clientSock, addr = serverSock.accept()

                # Check if we have a valid socket connection to a client
                #
                # When a clientSockection is found put it into the 
                # processing message queue.
                #
                self.communicateQueue.put([clientSock, addr])
                
                # Check if we should stop listening 
                #
                if self.stopServerVar == True:
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
                self.printQueue.put("\tConnection to '" + \
                    str(addr) + "' lost.")
                return 0

            # Append the data to the overall message
            #
            data += data_packet
        return data


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
            [clientSock, addr] = self.communicateQueue.get()
            # Get if queueEXIT STATUS is true. Stop thread if true.
            #
            if addr == self.CONST_EXIT_QUEUE:
                self.communicateQueue.task_done()
                break
            # Check if socket is still open
            #
            # Check if MSG is null to determine whether we are 
            # receiving or sending a message to client
            #
            self.printQueue.put("\t'" + str(addr) + "' - connected")
            
            # Receive the first four bytes containing the length    
            # of the message
            #
            raw_MSGLEN = self.__recvall__(clientSock, addr, 4)

            # Ensure the length of the message is not empty
            #
            if not raw_MSGLEN:
                clientSock.close()
                continue
            # Get the length of the message from the data header
            #
            MSGLEN = struct.unpack('>I', raw_MSGLEN)[0]
            self.printQueue.put("expected len message = " + str(MSGLEN))
            
            # Output the message sent by the client to message parser 
            # thread. Also pass the type of message
            #
            rawBuffer = self.__recvall__(clientSock, addr, MSGLEN)
            self.printQueue.put("actual len message =" + str(len(rawBuffer)))

            # Process RAW MESSAGE
            #
            self.__messageProcess__(clientSock, rawBuffer)

            # Client closed connect so we close connection too. 
            #
            self.printQueue.put("\t'" + str(addr) + "' - disconnected.")
            clientSock.close()

            # Indicate we finished processing the enqueued socket
            #
            self.communicateQueue.task_done()
        return 1

    # -- START FUNCTION DESCR --
    #
    # Decodes message based on its type
    #
    # Inputs:
    #   clientSocket = A live connection to a client sending a message
    #   rawBuffer = A message of type ToiChatProtocol received from client
    #
    # Outputs:
    #   - Hands off message to appropriate handler. 
    #
    # -- END FUNCTION DESCR --
    def __messageProcess__(self, clientSock, rawBuffer):
        # Create a ToiChat Message Type 
        #
        decodedToiMessage = ToiChatProtocol_pb2.ToiChatMessage()

        self.printQueue.put(rawBuffer)
        # Decode the raw message 
        #
        decodedToiMessage.ParseFromString(rawBuffer)

        # Find the type of message sent
        #
        msgType = decodedToiMessage.WhichOneof("messageType")
        if msgType == self.getType[0]:
            decodeDnsMsg = ToiChatProtocol_pb2.DnsMessage()
            decodeDnsMsg = decodedToiMessage
            self.printQueue.put(decodeDnsMsg)
            #handleDnsMessage(decodeDnsMsg)
        elif msgType == self.getType[1]:
            decodeChatMsg = ToiChatProtocol_pb2.ChatMessage()
            decodeDnsMsg = decodedToiMessage
            #handleChatMessage(decodeChatMsg)
        else:
            self.printQueue.put("Unknown MsgItem Type. '" + msgType + "'")
        return 1

    # -- START __FUNCTION DESCR --
    #
    # Processes print statement for server function and prints them
    # to a file. 
    #
    # Inputs:
    #   - A string seen on printQueue
    #
    # Outputs:
    #  - Prints to file 
    #
    # -- END FUNCTION DESCR --
    def __printToFile__(self):
        while True:
            # Get an item to print
            #
            text = self.printQueue.get()

            if text == self.CONST_EXIT_QUEUE:
                self.printQueue.task_done()
                break
            # Redirect print output to file
            #
            serverOut = open('toiChatServer.log', 'a')
            serverOut.write(str(text) + "\n")
            serverOut.close()
            # Indicate we finished processing the enqueued item to print
            #
            self.printQueue.task_done()
        return 0