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
import struct, sys
import conn_router
import gatewayIP
import time
# import DNSInstance

class toiChatserver():
    # -- START CLASS CONSTRUCTOR -- 
    #
    # ToiChat class handling client side communication
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, xHostname, xclientDescription=""):
        # Describe this toichatserver hostname/callsign
        #
        self.clientName = xHostname
        
        # Misc information about this toichat client
        #
        self.clientDescription = xclientDescription

        # Create a toiChatServer instance which we use to create messages
        #
        self.mytoiChatServer = toiChatServer(self.clientName, \
            self.clientDescription)

        # Create dns object instance
        #
        #self.DnsInstance = DNSInstance(self.clientName, self.clientDescription)

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
        #requestDNS = self.DnsInstance.requestDNSinfomation()
        requestDNS = DnsMessage()
        requestDNS.clientName = self.clientName
        requestDNS.clientId = socket.gethostbyname(socket.gethostname())
        requestDNS.lastUpdate = time.strftime("%Y%m%d - %H:%M:%S")
        requestDNS.description = self.clientDescription

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
                    pass
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
        # Start DNS server
        #
        #self.DnsInstance.start()

        # Request for DNS information from server we connected to
        #
        #self.DnsInstance.reqeustDNS(severIP)
        print("Connection to a server successful.")
        return 1

    
    # -- START FUNCTION DESCR --
    #
    # Sends a ToiChatMessage over a to a ToiChatSeve. This function will 
    # append the length of the message to the beginning to 
    # ensure the full message is sent. 
    #
    # Inputs:
    #  - toiServerIP = ToiChat server you wish to connect to
    #  - rawrawMSG = message type as defined by ToiChatMessage Protocol
    #  - outPut = Whether the message you are sending expects an output
    #
    # Outputs:
    #   - Returns true if message was sent successfully. 
    #
    # -- END FUNCTION DESCR -- 
    def sendMessage(self, toiServerIP, rawrawMSG, toiServerPORT=5005):
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
        decodedToiMessage.messageType = rawrawMSG

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

        # Close socket to server
        #
        serverSock.close()
        return 1