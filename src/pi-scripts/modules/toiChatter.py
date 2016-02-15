#!/usr/bin/env python3

# 
# Python toiChater
# Setups a communication channel for a user to talk to other users running
# the application
#
#
# Created on: 02/14/2016
# Author: Toi-Group
#
from modules.protobuf import ToiChatProtocol_pb2 # Used for ChatMessage 
                                                 # Protocol
from modules.toiChatClient import toiChatClient # Used for replying to 
                                                # received messages
import sys, readline # Used for overwriting current stdout line

class toiChatter():

    # Types of messages to expect as defined in ToiChatProtocol
    #
    getType={
        0:"one",
        1:"group"
    }

    # -- START CLASS CONSTRUCTOR -- 
    #
    # Upon start put user in chatting program
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self, toiChatClient, recipient):
        # Store ToiChatClient to used to send chat messages
        #
        self.myToiChatClient = toiChatClient

        # Store who we are talking to
        #
        self.recipient = recipient

    def startInstantMessage(self):
        print('-'*78)
        print("\nStart Chatting with : '" + str(self.recipient) + "'.\n")
        while True:
            # Wait for the user to send a message or keyboard interrupt
            #
            try:
                message = input(" >> ")
            except KeyboardInterrupt:
                break
            # Erase the current stdout prompt
            #
            sys.stdout.write("\033[F") # Move up cursor to previous line
            sys.stdout.write("\033[K") # Clear the current line

            # Print message you sent to the console
            #
            print(str(self.myToiChatClient.getName()) + ": " + \
                message)

            # Send your message to the recipient
            #
            self.sendOneChatMessage(message)
        # Close this chat instance
        #
        print("\nClosing Chat.")
        return 1

    # Handle a message from a client
    #
    def handleChatMessage(self, myChatMessage):
        # Erase the current stdout prompt but store it first
        # 
        sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')

        # Print the message from the receiver
        #
        sys.stdout.write(myChatMessage.id.clientName + ": " + \
            myChatMessage.textMessage + "\n")

        # Print the message that came before
        #
        sys.stdout.write(" >> " + readline.get_line_buffer())
        sys.stdout.flush()
        return 1

    # Return who this chatter's recipient currently is
    #
    def getRecipient(self):
        return self.recipient

    def sendOneChatMessage(self, textMessage):
        # Create a template DNS message
        #
        oneChatMessage = \
            self.myToiChatClient.createTemplateIdentifierMessage("chatMessage")

        # Populate who we are sending the message to
        #
        recipient = oneChatMessage.chatMessage.recipients.append(self.recipient)

        # Populate the textMessage with the message we want to send
        #
        oneChatMessage.chatMessage.textMessage = textMessage

        # Create a message to send
        #
        self.myToiChatClient.sendMessageByHostname(self.recipient, \
            oneChatMessage)