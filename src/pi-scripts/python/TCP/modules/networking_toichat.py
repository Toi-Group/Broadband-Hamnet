#!/usr/bin/env python3
# 
# Python Class:
#   networking_toichat 
#
# Created on: 02/01/2016
# Author: Toi-Group
#

import socket
from threading import Thread
import queue
import struct, sys

class networking_toichat():

    CONST_FIRSTCONNT = "FIRST MYIP="
    CONST_EXIT_THREAD = "EXITTHREAD"
    #CONST_BUFFERLEN = 2048

    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling network communication
    #   - Defaults to port = 5005
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xPORT_TOICHAT=5005):
        # Define port ToiChat uses to communicate
        #
        self.PORT_TOICHAT = xPORT_TOICHAT;

        # Create a client recv connection handler queue
        #
        self.q_send = queue.Queue()
        
        # Create a client message handler queue
        #
        self.q_rec = queue.Queue()
    
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
    # connections. The incoming socket is then handed off to a client
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
        
        # Start the client recv connection handler thread
        #
        C = Thread(target=self.__pi_process_client_toichat__)
        C.start()

        # Start the client message handler thread
        #
        M = Thread(target=self.__pi_process_message_toichat__)
        M.start()
        
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
        # stop the client recv connection handler thread
        #
        self.q_send.put(self.CONST_EXIT_THREAD)

        # Stop the client message handler thread
        #
        self.q_rec.put(self.CONST_EXIT_THREAD)
        
        return 1

    # -- START FUNCTION DESCR --
    #
    # Tries to connect to a ToiChat server. May raise an exception if 
    # connection is unsuccessful. 
    #
    # Inputs:
    #  - toiServerIP = ToiChat server to attempt connection to
    #
    # Outputs:
    #   - Returns true if connection was successful. 
    #
    # -- END FUNCTION DESCR -- 
    def attemptToiChatConn(self, toiServerIP):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set socket connection timeout
        #
        mySocket.settimeout(10) 

        # Try to connect to passed IP
        #
        mySocket.connect((toiServerIP, self.PORT_TOICHAT))

        # Connection to server successful. Tell the server to add you to 
        # a list of known hosts
        #
        self.__sendToiMessage__(mySocket, self.CONST_FIRSTCONNT + \
            str(socket.gethostbyname(socket.gethostname())))
        mySocket.close()
        return 1

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
        # Convert the message into binary
        #
        MSG = bytes(MSG, 'UTF-8')

        # Append the length of the message to the beginning
        #
        MSG = struct.pack('>I', len(MSG)) + MSG

        # Send the entire message.
        #
        mySocket.sendall(MSG)
        return 1

    # -- START FUNCTION DESCR -- 
    #
    # Open a port on the PI to act as the ToiChat server listener.
    #
    # Inputs:
    #  - PORT_TOICHAT = Port the server should listen on
    #
    # Outputs:
    #  - q_send = output is on the q_send queue that contains client 
    #           sockets waiting to be processed. 
    #
    #
    # -- END FUNCTION DESCR -- 
    def __pi_server_toichat__(self):
        # Create a tuple with listening on localhost and PORT_TOICHAT
        #
        SERVER = ('', self.PORT_TOICHAT)

        # Begin process of accepting incoming connection on designated port
        #
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Bind to localhost on PORT_TOICHAT 
            #
            s.bind(SERVER)

            # Allow for 5 clients to enter queue
            #
            s.listen(5)

            while True:
                conn, addr = s.accept()

                # When a connection is found put it into the processing
                # message queue.
                #
                self.q_send.put(conn)
        
        # If break out of loop print we are closing the sever
        #
        print("Closing ToiChat server")
        return 1

    # -- START FUNCTION DESCR -- 
    #
    # Process the information seen on the client socket that contacted the
    # ToiChat software
    #
    # Inputs:
    #  - q_send = input is on the q_send queue that contains messages 
    #       in string format received by client waiting to be processed. 
    #
    # Outputs:
    #  - q_rec = output is on the q_rec queue that contains messages
    #           in string format. 
    #
    # -- END FUNCTION DESCR -- 
    def __pi_process_client_toichat__(self):
        while True:
            # Get client request from server listen thread
            #
            conn = self.q_send.get()

            # Get if queueEXIT STATUS is true. Stop thread if true.
            #
            if conn == self.CONST_EXIT_THREAD:
                break
            
            # Receive the first packet containing the length of the message 
            #
            raw_MSGLEN = self.recvall(conn, 4)

            # Ensure the length of the message is not empty
            #
            if not raw_MSGLEN:
                conn.close()
                continue

            # Get the length of the message from the data header
            #
            MSGLEN = struct.unpack('>I', raw_MSGLEN)[0]

            # Output the message sent by the client to message parser.
            # Also, decode the data sent by the client
            #
            self.q_rec.put(bytes.decode(self.recvall(conn, MSGLEN), \
                'UTF-8'))

            # Close the connection to the client and get the next
            # item in the queue.
            #
            conn.close()
        return 1

    # -- START FUNCTION DESCR -- 
    #
    # From socket received message up to MSGLEN. 
    #
    # Inputs:
    #  - mysocket = socket connected a client machine
    #  - MSGLEN = received the message on the socket up to this length.
    #
    # Outputs:
    #  - data_packet = outputs message in binary format.
    #
    # Function Credit:
    # http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
    #
    # -- END FUNCTION DESCR -- 
    def recvall(self, mysocket, MSGLEN):

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
                print("Connection to client '" + str(clientIP) + "' lost.")
                return None

            # Append the data to the overall message
            #
            data += data_packet
        return data_packet
    
    # -- START FUNCTION DESCR -- 
    #
    # Processes the messages received by clients. Determines whether
    # we should add new host to known_hosts, start a chat, ect. 
    #
    # Inputs:
    #  - q_rec = input is on the q_rec queue that contains messages
    #       in string format waiting to be processed. 
    #
    # Outputs:
    #  None
    #
    # Function Credit:
    # http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
    #
    # -- END FUNCTION DESCR -- 
    def __pi_process_message_toichat__(self):
        while True:
            # Get message received from client
            #
            recMSG = self.q_rec.get()

            # Get if queue EXIT STATUS is true. Stop thread if true
            #
            if recMSG == self.CONST_EXIT_THREAD:
                break

            if self.CONST_FIRSTCONNT in recMSG:
                newHostIP = recMSG[len(self.CONST_FIRSTCONNT):]
                print("Found new host:" + newHostIP)

        return 1