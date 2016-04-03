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
import sys, readline, struct,fcntl,termios # Used for overwriting current 
                                           # stdout line
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
    def __init__(self, toiChatClient, recipient, textView):
        # Store ToiChatClient to used to send chat messages
        #
        self.myToiChatClient = toiChatClient

        # Store who we are talking to
        #
        self.recipient = recipient

        #Store textView object
        #
        self.myTextView = textView

    def startInstantMessage(self):
        # Clear the console
        #
        print(chr(27) + "[2J") 

        # Print connection info
        #
        print("Start Chatting with : '" + str(self.recipient) + "'.\n" + 
            "(Escape Sequence: Ctrl+c)")
        
        # Print line separator
        #
        print('-'*78 + "\n")

        while True:
            # Wait for the user to send a message or keyboard interrupt
            #
            try:
                message = input(" >> ")
            except KeyboardInterrupt:
                break
            # Following lines sourced from stackoverflow
            #
            # http://stackoverflow.com/questions/2082387/reading-input-from-raw-input-without-having-the-prompt-overwritten-by-other-th
            # Next line said to be reasonably portable for various Unixes
            (rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, \
                termios.TIOCGWINSZ,'1234'))

            text_len = len(message)+2

            # ANSI escape sequences (All VT100 except ESC[0G)
            # Move up cursor to previous line
            #
            sys.stdout.write("\033[F")

            # Clear current line
            #
            sys.stdout.write('\x1b[2K') 

            # Move cursor up and clear line
            #
            sys.stdout.write('\x1b[1A\x1b[2K'*int(text_len/cols))
            
            # Move to start of line
            #
            sys.stdout.write('\x1b[0G')
            sys.stdout.flush()

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

        # Print received message
        #
        self.buffer = self.myTextView.get_buffer()
 
        self.iter = self.buffer.get_iter_at_offset(-1)

        self.buffer.insert(self.iter,("\n" + myChatMessage.id.clientName + " : " + myChatMessage.textMessage))

        self.myTextView.set_buffer(self.buffer)


        return (1)

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
