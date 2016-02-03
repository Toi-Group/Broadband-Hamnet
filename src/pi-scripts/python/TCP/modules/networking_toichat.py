#!/usr/bin/env python3
# 
# Python Class:
#   toiChatServer 
#   toiChatClient 
#
# Created on: 02/01/2016
# Author: Toi-Group
#

from protobuf.ToiChatProtocol import ToiChatMessage
import socket
from threading import Thread
import queue
import struct, sys

# ToiChat Server listener
#
class toiChatServer():

    CONST_EXIT_THREAD = "EXITTHREAD"

    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling server side communication handling
    #   - Defaults to port = 5005
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xPORT_TOICHAT=5005):
        # Define port ToiChat uses to communicate
        #
        self.PORT_TOICHAT = xPORT_TOICHAT;

        # Create a client recv clientSockection handler queue
        #
        self.socketClientQueue = queue.Queue()
        
    
    # -- START CLASS DESTRUCTOR -- 
    #
    # ToiChat class destructor stops background threads upon class delete
    #
    # -- END CLASS DESTRUCTOR -- 
    def __del__(self):
        self.stopServer
    
    # -- START FUNCTION DESCR --
    #
    # Starts a thread listening on PORT_TOICHAT for incoming socket 
    # clientSockections. The incoming socket is then handed off to a client
    # recv thread to receive the full message. Finally the message
    # is handed off to a message handler thread to determine what to do
    # with the received message.
    #
    # Inputs:
    #  None
    #
    # Outputs:
    #   - Three threads to manage BG application services.  
    #
    # -- END FUNCTION DESCR -- 
    def startServer(self):
        # Start the server listener thread
        #
        S = Thread(target=self.__pi_server_toichat__)
        S.daemon = True
        S.start()
        
        # Start the client recv clientSockection handler thread
        #
        C = Thread(target=self.__talkClient__)
        C.start()

        return 1

    # -- START FUNCTION DESCR --
    #
    # Stop all threads created by startServer
    #
    # Inputs:
    #  None
    #
    # Outputs:
    #   - Stops two threads to manage BG application services. The third
    #       server_listener thread was a daemon process that will close
    #       upon application closure. 
    #
    # -- END FUNCTION DESCR -- 
    def stopServer(self):
        # stop the client recv clientSockection handler thread
        #
        self.socketClientQueue.put([self.CONST_EXIT_THREAD, ''])

        return 1

    # -- START FUNCTION DESCR -- 
    #
    # Open a port on the PI to act as the ToiChat server listener.
    #
    # Inputs:
    #  - PORT_TOICHAT = Port the server should listen on
    #
    # Outputs:
    #  - socketClientQueue = output is on the socketClientQueue queue that  
    #       contains client sockets waiting to be processed. 
    #
    #
    # -- END FUNCTION DESCR -- 
    def __pi_server_toichat__(self):
        # Create a tuple with listening on localhost and PORT_TOICHAT
        #
        SERVER = ('', self.PORT_TOICHAT)

        # Begin process of accepting incoming clientSockection on designated port
        #
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind to localhost on PORT_TOICHAT 
            #
            s.bind(SERVER)

            # Allow for 5 clients to enter queue
            #
            s.listen(5)

            while True:
                clientSock, addr = s.accept()

                # When a clientSockection is found put it into the processing
                # message queue.
                #
                self.socketClientQueue.put(clientSock)
        
        # If break out of loop print we are closing the sever
        #
        print("Closing ToiChat server")
        return 1

    # -- START FUNCTION DESCR -- 
    #
    # Processes the client seen on socket that contacted the
    # ToiChat software. 
    #
    # Inputs:
    #  - socketClientQueue = input is on the socketClientQueue that  
    #       clientSock connections
    #
    # Outputs:
    #  - None
    #
    # -- END FUNCTION DESCR -- 
    def __talkClient__(self):
        while True:
            # Get a client socket clientSockection from server listen thread
            #
            clientSock = self.socketClientQueue.get()

            # Get if queueEXIT STATUS is true. Stop thread if true.
            #
            if clientSock == self.CONST_EXIT_THREAD:
                break
            
            # Receive the first four bytes containing the length of the  
            # message
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
            rawToiChatBuffer = self.__recvall__(clientSock, MSGLEN))
            
            # Process RAW MESSAGE
            __processMessage__(clientSock, rawToiChatBuffer)

            # Close the clientSockection to the client and get the next
            # item in the queue.
            #
            clientSock.close()
        return 1


    # -- START FUNCTION DESCR --
    #
    #
    #
    # Inputs:
    #
    #
    # Outputs:
    # 
    #
    # -- END FUNCTION DESCR --
    def __processMessage__(self, clientSocket, rawToiChatBuffer):
        #Convert from raw binary data
        #
        myToiChatMessage.ParseFromString(rawToiChatBuffer)
        
        # Gather Header Information
        #
        clientName = myToiChatMessage.clientName
        clientId = myToiChatMessage.clientId
        description = myToiChatMessage.description

        for MsgItem in myToiChatMessage:
            if MsgItem.ItemType == getType(0):
                handleDnsNewClient(MsgItem)
            elif MsgItem.ItemType == getType(1):
                handleRequestDns(clientSocket, MsgItem)
            else:
                print("Unknown MsgItem Type.")

    # -- START DICTIONARY DECLARATION --
    #
    # Dictionary containing message numeric id with 
    #
    # Inputs:
    #  None
    #
    # Outputs:
    #   - Three threads to manage BG application services.  
    #
    # -- END FUNCTION DESCR -- 
    MSG_TYPE = {
        0: ToiChatMessage.RegClient,
        1: ToiChatMessage.RequestArp,
        2: ToiChatMessage.SendArp,
        3: ToiChatMessage.OneToOne,
    }

    # -- START FUNCTION DESCR --
    #
    # Returns the message type
    #
    # Inputs:
    #  None
    #
    # Outputs:
    #   - Three threads to manage BG application services.  
    #
    # -- END FUNCTION DESCR -- 
    def getType(in):
        return MSG_TYPE[in]

    # -- START FUNCTION DESCR -- 
    #
    # From socket received message up to MSGLEN. 
    #
    # Inputs:
    #  - mysocket = socket clientSockected a client machine
    #  - MSGLEN = received the message on the socket up to this length.
    #
    # Outputs:
    #  - data_packet = outputs message in binary format.
    #
    #
    # -- END FUNCTION DESCR -- 
    def __recvall__(self, mysocket, MSGLEN):

        # Get the client's IP
        #
        clientIP = mysocket.getpeername()

        # Initiate an array with the message being sent by client
        #
        data = b''
        
        # While the client is still sending a message
        #
        while len(data) < MSGLEN:
            # Keep reading message from client
            #
            data_packet = mysocket.recv(MSGLEN - len(data))
            if not data_packet:
                print("clientSockection to client '" + str(clientIP) + "' lost.")
                return None

            # Append the data to the overall message
            #
            data += data_packet
        return data_packet

# ToiChat Client Talker
#
class toiChatClient():

    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling client side communication
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xHostname, xIP, xDescription):
        # Create a ToiChatClient containing this machines information
        #
        self.myToiChat = ToiChatProtocol.ToiChatClientRunner()
        self.myToiChat.clientName = xHostname
        self.myToiChat.clientId = xIP
        self.myToiChat.description = xDescription        
    
    # -- START CLASS DESTRUCTOR -- 
    #
    # 
    #
    # -- END CLASS DESTRUCTOR -- 
    def __del__(self):

    # -- START FUNCTION DESCR --
    #
    # Asks server to register the list of ChatRunners seen in lstChatRunner
    #
    # Inputs:
    #   lstChatRunner = list of ToiChatClientRunner messages
    #
    # Outputs:
    # 
    #
    # -- END FUNCTION DESCR --
    def doRegClient(serverSocket, lstChatRunner):
        # Create a new DnsRegisterRequest
        #
        dnsRegister = ToiChatProtocol.DnsRegisterRequest()
        dnsRegister.registerBy = self.myToiChat

        # Loop through each item in list of items to register
        #
        for chatRunner in lstChatRunner:
            dnsRegister.clientList.add(chatRunner)

        # Send populated dnsRegister Request to Server
        #
        __sendToiMessage__(serverSocket, dnsRegister.SerializeToString())

        # Await response saying it was a success
        #


        # Return serialized data containing message
        #
        return 1

    # -- START FUNCTION DESCR --
    #
    # Tries to clientSockect to a ToiChat server. May raise an exception if 
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
    def attemptServer(self, toiServerIP, PORT_TOICHAT=5005):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket clientSockection timeout
        #
        serverSocket.settimeout(10) 

        # Try to clientSockect to passed IP
        #
        serverSocket.clientSockect((toiServerIP, PORT_TOICHAT))
        
        # If successful connection, tell the server to register this machine in it DNS
        #
        RegClient(serverSocket, myToiChat)

        serverSocket.close()
        return 1

    # -- START FUNCTION DESCR --
    #
    #
    #
    # Inputs:
    #
    #
    # Outputs:
    # 
    #
    # -- END FUNCTION DESCR --
    def __processMessage__(self, serverSocket, rawToiChatBuffer):
        #Convert from raw binary data
        #
        myToiChatMessage.ParseFromString(rawToiChatBuffer)
        

    # -- START FUNCTION DESCR --
    #
    # Sends a message to the server seen on the socket. This function
    # will append the length of the message to the beginning to ensure
    # the full message is sent. 
    #
    # Inputs:
    #  - mySocket = Server to send message to
    #  - MSG = Message user is trying to send
    #
    # Outputs:
    #   - Returns true if message was sent successfully. 
    #
    # -- END FUNCTION DESCR -- 
    def __sendToiMessage__(self, mySocket, MSG):

        # Append the length of the message to the beginning
        #
        MSG = struct.pack('>I', len(MSG)) + MSG

        # Send the entire message.
        #
        mySocket.sendall(MSG)
        return 1