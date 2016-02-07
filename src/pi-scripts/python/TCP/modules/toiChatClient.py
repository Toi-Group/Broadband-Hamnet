#!/usr/bin/env python3
# 
# Python toiChat Class:
#   Services: 
#       toiChatserver 
#
# Created on: 02/04/2016
# Author: Toi-Group
#

from modules.protobuf import ToiChatProtocol_pb2
import socket
import struct, sys
from modules.conn_router import conn_router
from modules.gatewayIP import gatewayIP
import time

# import DNSInstance

class toiChatClient():
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
        requestDNS = ToiChatProtocol_pb2.ToiChatMessage()
        requestDNS.dnsMessage.command = 0
        requestDNS.dnsMessage.clientName = self.clientName
        requestDNS.dnsMessage.clientId = socket.gethostbyname(socket.gethostname())
        requestDNS.dnsMessage.lastUpdate = time.strftime("%Y%m%d - %H:%M:%S")
        requestDNS.dnsMessage.description = "Lorem Ipsum is simply dummy" + \
        "text of the printing and typesetting industry. Lorem Ipsum has " + \
        "been the industry's standard dummy text ever since the 1500s, " + \
        "when an unknown printer took a galley of type and scrambled it " +\
        "to make a type specimen book. It has survived not only five " + \
        "centuries, but also the leap into electronic typesetting, " + \
        "remaining essentially unchanged. It was popularised in the 1960s " + \
        "with the release of Letraset sheets containing Lorem Ipsum " + \
        "passages, and more recently with desktop publishing software " + \
        "like Aldus PageMaker including versions of Lorem Ipsum.It is a " + \
        "long established fact that a reader will be distracted by the " + \
        "readable content of a page when looking at its layout. The point " + \
        "of using Lorem Ipsum is that it has a more-or-less normal distribution" + \
        " of letters, as opposed to using 'Content here, content here', " + \
        "making it look like readable English. Many desktop publishing " + \
        "packages and web page editors now use Lorem Ipsum as their default " + \
        "model text, and a search for 'lorem ipsum' will uncover many web sites " + \
        "still in their infancy. Various versions have evolved over the " + \
        "years, sometimes by accident, sometimes on purpose (injected " + \
        "humour and the like).Contrary to popular belief, Lorem Ipsum is " + \
        "not simply random text. It has roots in a piece of classical " + \
        "Latin literature from 45 BC, making it over 2000 years old. "

        requestDNSTest = ToiChatProtocol_pb2.DnsMessage.DNSClients()
        
        for x in range(0, 100):
            requestDNSTest = requestDNS.dnsMessage.nums.add()
            requestDNSTest.clientName = requestDNS.dnsMessage.clientName
            requestDNSTest.clientId  = requestDNS.dnsMessage.clientId 
            requestDNSTest.lastUpdate = requestDNS.dnsMessage.lastUpdate
            requestDNSTest.description = requestDNS.dnsMessage.description

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
    def sendMessage(self, toiServerIP, decodedToiMessage, \
        toiServerPORT=5005):
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

        # Convert ToiChatMessage to binary stream.
        # 
        encodedToiMessage = decodedToiMessage.SerializeToString()
        print("len of message = " + str(len(encodedToiMessage)))
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
        return 1