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

from modules.protobuf import ToiChatProtocol_pb2 # Used for decoding 
                                                 # and finding message type
                                                 # of a ToiChatMessage
import socket # Used for receiving information from a toiChatClient
from threading import Thread # Used for separating listener with server 
                            # full message receiver. 
import queue # Used for communication between server listener, receiver, 
             # and printer
import struct, sys # Used for finding the full message length of a received
                   # message.
import time # Used for cataloging the date in server logs.
import readline # Used for reading in stdout to print to console now.

# ToiChatServer listener and ToiChatMessage handler
#
class toiChatServer():

    # String constant to send to queues when they should quit
    #
    CONST_EXIT_QUEUE = "EXITTHREAD"

    # Types of messages to expect as defined in ToiChatProtocol
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
    def __init__(self, toiChatNameServer, PORT_TOICHAT=5005, \
        logFileName = 'toiChatServer.log'):
        # Filename where should we save server logs to
        #
        self.logFileName = logFileName

        # Store ToiChatNameServer to use
        #
        self.myToiChatNameServer = toiChatNameServer

        # Define port ToiChat uses to communicate
        #
        self.PORT_TOICHAT = PORT_TOICHAT;

        # Handle multiple chat instances
        #
        self.myToiChatters = []

        # Server is by default set to disabled
        #
        self.stopServerVar = False

        # Create a communication handler thread queue
        #
        self.communicateQueue = queue.Queue()

        # Create a print to file queue
        #
        self.printQueue = queue.Queue()

        # Create a print to stdout Now queue
        #
        self.printQueueNow = queue.Queue()

        # Create the client recv connection handler thread
        #
        self.S = Thread(target=self.__toiChatListener__)

        # Create the communication handler thread
        #
        self.C = Thread(target=self.__communicate__)

        # Print server output to file thread
        #
        self.W = Thread(target=self.__printToFile__)
        self.W.daemon = True
        self.W.start()

        # Print server output to user Now thread
        #
        self.N = Thread(target=self.__printToUserNow__)
        self.N.daemon = True
        self.N.start()
    
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
        self.stopServerVar = False
        # Check to see if printer thread has already started
        #
        if (self.W.is_alive() == False):
            try:
                self.W.start()
            except RuntimeError as e:
                raise Exception("ERROR: ToiChatServer printer thread " + \
                    "failed to start! - " + str(e))
                return 0        
        self.printQueue.put("Attempting to start ToiChat server...")
        self.printQueue.put("Print Server thread started.", \
            True)

        # Check to see if server listener thread has already started
        #
        if (self.S.is_alive() == False):
            self.stopServerVar = False
            # Attempt to start the server listener
            #
            try:
                self.S.start()
            except RuntimeError as e:
                self.printQueue.put("ERROR: ToiChatServer server listener " + \
                    "thread failed to start! - " + str(e), True)
                raise Exception("ERROR: ToiChatServer server listener " + \
                    "thread failed to start! - " + str(e))
                return 0
        self.printQueue.put("Server Listener " + \
            "thread started.", True)

        # Check to see if message processor thread has already started
        #
        if (self.C.is_alive() == False):
            try:
                # Attempt to start the message processor thread
                #
                self.C.start()
            except RuntimeError as e:
                self.printQueue.put("ERROR: ToiChatServer message " + \
                    "processor thread failed to start! - " + str(e), True)
                raise Exception("ERROR: ToiChatServer message processor " + \
                    "thread failed to start! - " + str(e))
                return 0
        self.printQueue.put("Message Processor " + \
                "thread started.", True)

        # Server dependencies started successfully.
        #
        self.printQueue.put("Attempt to start server was successful!\n")
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

        if (self.S.is_alive() == True):
            # Tell the server listener thread to break accepting connections
            #
            self.stopServerVar = True

            # Connect to this toiChatServer instance to break out of
            # accept statement in server listener thread
            #
            serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSock.connect(('', self.PORT_TOICHAT))
            serverSock.close()

            # Wait for server thread to close
            #
            self.S.join(3.0)
        
        if (self.C.is_alive() == True):
            # Stop the communicateQueue thread handler 
            # 
            self.communicateQueue.put([None, self.CONST_EXIT_QUEUE])
            
            # Wait for server thread to close
            #
            self.C.join(3.0)

        # Determine if server listener thread stopped correctly
        #
        if (self.S.is_alive() == True and self.C.is_alive() == False):
            self.printQueue.put("Attempt to stop server listener failed.\n")
            del self.C
            # Create the communication handler thread
            #
            self.C = Thread(target=self.__communicate__)
            # Restart server to ensure all threads are running correctly
            #
            self.startServer()
            return 0
        elif (self.S.is_alive() == False and self.C.is_alive == True):
            del self.S
            self.printQueue.put("Attempt to stop message handler failed.\n")
            # Create the client recv connection handler thread
            #
            self.S = Thread(target=self.__toiChatListener__)
            # Restart server to ensure all threads are running correctly
            #
            self.startServer()
            return 0
        self.printQueue.put("Attempt to stop server was successful!\n")
        # Create new instances of the threads
        del self.C
        del self.S

        # Create the client recv connection handler thread
        #
        self.S = Thread(target=self.__toiChatListener__)

        # Create the communication handler thread
        #
        self.C = Thread(target=self.__communicate__)
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

    # -- START FUNCTION DESCR --
    #
    # Updates the port the server listener work on.
    #
    # Inputs:
    #   None
    #
    # Outputs:
    #   - Returns true if server is running else fase.
    #
    # -- END FUNCTION DESCR -- 
    def updateServerPort(self, PORT_TOICHAT=5005):
        # Define port ToiChat uses to communicate
        #
        self.PORT_TOICHAT = PORT_TOICHAT
        
        # Print that we are restarting the server
        #
        self.printQueue.put("We are restarting the server threads...")
        self.stopServer()
        self.startServer()
        return 1

    # -- START FUNCTION DESCR --
    #
    # Update Chat Message Handler array
    #
    # Inputs:
    #   A toiChatter Instance
    #
    # Outputs:
    #   Updated internal toiChatter handler with inputted toiChatter Instance
    #   added to handler array
    #
    # -- END FUNCTION DESCR --
    def addToiChatter(self, toiChatter):
        self.myToiChatters.append(toiChatter)
        return 1

    # -- START FUNCTION DESCR --
    #
    # Update Chat Message Handler array
    #
    # Inputs:
    #   A toiChatter Instance
    #
    # Outputs:
    #   Updated internal toiChatter handler with inputted toiChatter Instance
    #   removed from handler array
    #
    # -- END FUNCTION DESCR --
    def removeToiChatter(self, toiChatter):
        try:
            self.myToiChatters.remove(toiChatter)
        except ValueError:
            pass
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
    def __toiChatListener__(self):
        # Create a tuple with listening on localhost and PORT_TOICHAT
        #
        SERVER = ('', self.PORT_TOICHAT)

        # Begin process of accepting incoming clientSockection on 
        # designated port
        #
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSock:
            # Set socket lifetime after close to none
            #
            # See http://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
            serverSock.setsockopt(socket.SOL_SOCKET, \
                socket.SO_REUSEADDR, 1)

            # Bind to localhost on PORT_TOICHAT 
            #
            serverSock.bind(SERVER)

            # Allow for 5 clients to enter queue
            #
            serverSock.listen(5)

            while True:
                # Accept incoming client connections
                #
                clientSock, addr = serverSock.accept()

                # Check if we should stop listening based on variable
                # and if connection was from ourselves
                #
                if (self.stopServerVar == True) and \
                        (str(addr[0]) == "127.0.0.1"):
                    serverSock.close()
                    break

                # Check if we have a valid socket connection to a client
                #
                # When a clientSockection is found put it into the 
                # processing message queue.
                #
                self.communicateQueue.put([clientSock, addr])
        return 1

    # -- START FUNCTION DESCR -- 
    #
    # Processes the message with toiChatClient seen on socket passed
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

            # Check if socket is still open?
            #

            # Print to log we are receiving a message
            #
            self.printQueue.put(str(addr) + " - connected")
            
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
            self.printQueue.put("expected len message = " + str(MSGLEN), \
                True)
            
            # Continue receiving the full message expected from client
            #
            rawBuffer = self.__recvall__(clientSock, addr, MSGLEN)
            self.printQueue.put("actual len message = " + \
                str(len(rawBuffer)), True)

            # Process RAW MESSAGE
            #
            self.__messageProcess__(clientSock, rawBuffer)

            # Close socket to client. 
            #
            self.printQueue.put(str(addr) + " - disconnected.")
            clientSock.close()

            # Indicate we finished processing the enqueued socket
            #
            self.communicateQueue.task_done()
        return 1

    # -- START FUNCTION DESCR -- 
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
                self.printQueue.put("Connection to '" + \
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
    # Decodes message based on its type
    #
    # Inputs:
    #   - clientSocket = A live connection to a toiChatClient that
    #       sent a message
    #   - rawBuffer = A message of type ToiChatProtocol received from client
    #
    # Outputs:
    #   - Hands off message to appropriate handler. 
    #
    # -- END FUNCTION DESCR --
    def __messageProcess__(self, clientSock, rawBuffer):
        # Create a ToiChat Message Type 
        #
        decodedToiMessage = ToiChatProtocol_pb2.ToiChatMessage()

        self.printQueue.put("RAW Received MSG = " + str(rawBuffer))
        # Decode the raw message 
        #
        decodedToiMessage.ParseFromString(rawBuffer)

        # Find the type of message sent
        #
        msgType = decodedToiMessage.WhichOneof("messageType")
        if msgType == self.getType[0]:
            decodeDnsMsg = ToiChatProtocol_pb2.DnsMessage()
            decodeDnsMsg = decodedToiMessage.dnsMessage
            self.printQueue.put("Decoded Received MSG = " + \
                str(decodeDnsMsg))
            self.myToiChatNameServer.handleDnsMessage(decodeDnsMsg)
            return 1
        elif msgType == self.getType[1]:
            decodeChatMsg = ToiChatProtocol_pb2.ChatMessage()
            decodeChatMsg = decodedToiMessage.chatMessage
            self.printQueue.put("Decoded Received MSG = " + \
                str(decodeChatMsg))
            # We check what toiChatter message belongs to
            #
            if self.myToiChatters:
                # Loop over each toiChatter the server has access to
                #
                for chatter in self.myToiChatters:
                    # Check to see if chatter recipient matches sender id
                    #
                    if chatter.getRecipient() == \
                        str(decodeChatMsg.id.clientName):
                        chatter.handleChatMessage(decodeChatMsg)
                return 1
                # If after loop we still don't know who message is from
                # prompt user that he has a new message
                #
            self.printQueueNow.put("You have a new message from : " + \
                str(decodeChatMsg.id.clientName) + ". Open a chat " + \
                "window to talk back.")
            return 1
        self.printQueue.put("Unable to Process Message of type. '" \
            + msgType + "'")
        return 0

    # -- START __FUNCTION DESCR --
    #
    # Processes print statement for server function and prints them
    # to a file. 
    #
    # Inputs:
    #   - A string seen on printQueue
    #
    # Outputs:
    #  - Prints to log file 
    #
    # -- END FUNCTION DESCR --
    def __printToFile__(self, subMessage=False):
        while True:
            # Get an item to print
            #
            text = self.printQueue.get()

            if text == self.CONST_EXIT_QUEUE:
                self.printQueue.task_done()
                break
            # Redirect print output to file
            #
            serverOut = open(self.logFileName, 'a')

            if subMessage == False:
                serverOut.write(time.strftime("%Y%m%d - %H:%M:%S") + \
                    " - " + str(text) + "\n")
            else:
                serverOut.write("\t" + time.strftime("%Y%m%d - %H:%M:%S") + \
                    " - " + str(text) + "\n")
            serverOut.close()

            # Indicate we finished processing the enqueued print request
            #
            self.printQueue.task_done()
        return 0

    # -- START __FUNCTION DESCR --
    #
    # Processes print statement for server function and prints them
    # to a file. 
    #
    # Inputs:
    #   - A string seen on printQueueNow
    #
    # Outputs:
    #  - Prints to stdout
    #
    # -- END FUNCTION DESCR --
    def __printToUserNow__(self):
        while True:
            # Get an item to print
            #
            text = self.printQueueNow.get()

            if text == self.CONST_EXIT_QUEUE:
                self.printQueue.task_done()
                break
            # Erase the current stdout prompt but store it first
            # 
            sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
            
            # Print the message from the receiver
            #
            sys.stdout.write(text + "\n")

            # Print the message that came before
            #
            sys.stdout.write(" >> " + readline.get_line_buffer())

            # Indicate we finished processing the enqueued print request
            #
            self.printQueueNow.task_done()
        return 0