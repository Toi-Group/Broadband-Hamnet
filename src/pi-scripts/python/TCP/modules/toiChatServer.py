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

import protobuf.ToiChatProtocol_pb2
import socket
from io import StringIO
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

        # Server is by default set to disabled
        #
        self.stopServer = False

        # Create a communication handler thread queue
        #
        self.communicateQueue = queue.Queue()

        # Start the client recv connection handler thread
        #
        self.S = Thread(target=self.__pi_server_toichat__)

        # Start the communication handler thread
        #
        self.C = Thread(target=self.__communicate__)
        self.C.daemon = True

    
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
    #   - A thread running server listen serverMsg.operations running
    #
    # -- END FUNCTION DESCR -- 
    def startServer(self):
        print("Attempting to start ToiChat server...")

        # Check to see if server listener thread has already started
        #
        if (self.S.is_alive() == False):
            self.stopServer = False
            # Attempt to start the server listener
            #
            try:
                self.S.start()
            except RuntimeError as e:
                print("\tAttempt to start server failed.\n\n")
                return -1
        # Check to see if message processor thread has already started
        #
        elif (self.C.is_alive() == False):
            try:
                # Attempt to start the message processor thread
                #
                self.C.start()
            except RuntimeError as e:
                print("\tAttempt to start server failed.\n\n")
                return -1
        # Both server dependencies are already started
        #
        else:
            print("\tServer already started.\n\n")
            return 1
        # Server dependencies started successfully.
        #
        print("\tAttempt to start server was successful!\n\n")
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
        print("Attempting to stop ToiChat server...")

        # Tell the server listener thread to break accepting connections
        #
        self.stopServer = True

        # Stop the communicateQueue thread handler 
        # 
        self.communicateQueue.put(self.CONST_EXIT_THREAD)

        # Wait for both server threads to close
        #
        self.S.join(3.0)
        self.C.join(3.0)

        # Determine if server listener thread stopped correctly
        #
        if (self.S.is_alive() or self.C.is_alive()) == True:
            print("\tAttempt to stop server failed.\n\n")
            return -1
        else:
            print("\tAttempt to stop server was successful!\n\n")
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
            return -1

        # -- START FUNCTION DESCR --

    #
    # Sends commands to a ToiChatServer instance to perform operations
    # remotely. May raise an exception if toiChatServer can not be reached
    #
    # Inputs:
    #   - whoSend = (Multiple Possibilities)
    #       - A IPv4 Address which the function will lookup using the
    #           internal DNS instance
    #       - A already open socket which we will reply to. Assumed input
    #           from __handleServerMessage__ function
    #   - serverMsg = (Multiple Possibilities)
    #       - A string input containing a server command
    #       - A predefined ServerMessage. Assumed input from
    #            __handleServerMessage__ function
    # Outputs:
    #   None
    #
    # -- END FUNCTION DESCR --
    def createRemoteServerMessage(self, msgCMD):
        # Create a New Server Message with the command seen from serverMsg
        #
        if msgCMD.lower() == ("stop" or "start" or "status"):
            myServerMessage = ServerMessage()
            # Create the server message with the appropriate command
            #
            if serverMsg == "stop":
                reponseMessage.operation = "STOP"
            elif serverMsg == "start":
                reponseMessage.operation = "START"
            else:
                reponseMessage.operation = "STATUS"
            
            # The the message with the correct command
            #
            return serverMsg
        else:
            self.printServerUsage()
            return -1

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
            serverSock.settimeout(2) 

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
                if self.stopServer == True:
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
                print("\tConnection to '" + \
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
                if MSG == None:
                    # Print that we have a new connection
                    #
                    clientIP = clientSock.getpeername()

                    print("'" + str(clientIP) + "'' - connected")
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
                    rawBuffer = self.__recvall__(clientSock, MSGLEN)

                    # Process RAW MESSAGE
                    #
                    self.__messageProcess__(clientSock, rawBuffer)
                else:
                    # We are sending information back to the client
                    #
                    return self.__sendToiChatMessage__(clientSock, MSG)

            # Client closed connect so we close connection too. 
            #
            print("\t'" + str(clientIP) + "' - disconnected.")
            clientSock.close()
        return 1

    # -- START __FUNCTION DESCR --
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
            handleDnsMessage(clientSock, decodeDnsMsg)
        elif msgType == self.getType[1]:
            decodeServerMsg = ServerMessage()
            decodeServerMsg.ParseFromString(decodedToiMessage)
            self.__handleServerMessage__(clientSock, decodeServerMsg)
        else:
            print("Unknown MsgItem Type.")
        return

    # -- START FUNCTION DESCR --
    #
    # 
    #
    # Inputs:
    #
    # Outputs:
    # 
    #
    # -- END FUNCTION DESCR --
    def __handleServerMessage__(self, clientSock, serverMsg):
        # Check Against possible known server messages
        #
        # Response type messages
        #
        if serverMsg.operation == ("SUCCESS" or "FAILED" or "UNKOWN") :
            # Message type does not invoke a response so we close the
            # socket to the client
            #
            clientSock.close()

            # Print that connection to client closed
            #
            print(str(clientIP) + " - connected")
            # Print Message sent by server
            #
            print(serverMsg.operation + serverMsg.msgDescription)
            self.communicateQueue.put([clientSock, None])
            return 1
        # Command Type messages
        #
        elif serverMsg.operation == ("STOP" or "START" or "STATUS"):
            # Capture output of server to variable
            #
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = mystdout = StringIO()
            sys.stdout = mystderr = StringIO()

            responseMsgDescription = ""
            # Perform command
            #
            if serverMsg.operation == "STOP":
                operationStatus = self.stopServer()
            elif serverMsg.operation == "START":
                operationStatus = self.startServer()
            # If the remote server is asking for status return that we
            # are alive and responding.
            #
            elif serverMsg.operation == "STATUS":
                operationStatus = self.statusServer()
            
            # Create response server message
            #
            reponseMessage = ServerMessage()
            reponseMessage.description = mystdout
            reponseMessage.descriptionErr = mystderr

            # Reset stdout and stderr back to console
            #
            sys.stdout = old_stdout
            sys.sys.stderr = old_stderr

            # Check if command was successful
            #
            if operationStatus == 1:
                reponseMessage.operation = "SUCCESS"
                self.communicateQueue.put([clientSock, reponseMessage])
                return 1
            else:
                reponseMessage.operation = "FAILED"
                self.communicateQueue.put([clientSock, reponseMessage])
                return -1
           #
           # We do not close the clientSocket since we expect a response
           #

        # If could not recognize the response || command message type
        # return UkNOWN to send server
        #
        else:
            # Create response server message
            #
            reponseMessage = ServerMessage()
            reponseMessage.operation = "UNKOWN"
            reponseMessage.description = "The server" + \
                "message command '" + serverMsg.operation +"' you " +\
                "sent was not recognized"

            # Tell the receiving client the command is not known
            #
            self.createRemoteServerMessage(clientSock, reponseMessage)

            # Message type does not invoke a response so we close the
            # socket to the client
            #
            clientSock.close()
            return -1

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
    def __sendToiChatMessage__(self, clientSock, rawMsg):
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

        # Put message on communicate queue.
        #
        self.communicateQueue.put([clientSock, encodedToiMessage])
        return 1