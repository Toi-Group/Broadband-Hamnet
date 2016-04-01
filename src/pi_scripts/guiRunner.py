#!/usr/bin/env python3

#
#Python toiChat GUI
#    interfaces with all back-end chat program for ease of use with user
# 
#
#
#   
#Created on: 03//30/16
#Author: Toi-Group
#


import sys #used for exiting the program
import threading #used for threading instances to update gui graphics and run backend software in sudo-parallel
from modules.toiChatServer import toiChatServer #Backend server software
from modules.toiChatClient import toiChatClient #backend client software
from modules.toiChatter import toiChatter #backend chat software to allow chat messaging
from modules.toiChatNameServer import toiChatNameServer #backend DNS software
from modules.testSSH import * #script to load router scripts from python execution to implement toiChat-RMDP (Remote Machine Discovery Protocol)
from gi.repository import Gtk, GObject #GUI and threading library


class ToiChatGui():
    
    # -- START CLASS CONSTRUCTOR --
    #
    # Upon instantiation parses glade XML file 
    # and connects signals to functions
    # also shows main login window
    #
    # -- END CLASS CONSTRUCTOR -- 
    def __init__(self):
        #Load glade file for login window
        #initilize all buttons and entry boxes
        #Login window
        #
        self.builder = Gtk.Builder()
        self.builder.add_from_file('toiTest.glade')
        self.login_window = self.builder.get_object('mainWindow')
        self.userName = self.builder.get_object('user_name')
        self.passWord = self.builder.get_object('pass_word')
        self.miscellaneous = self.builder.get_object('misc')
        self.errorMessage = self.builder.get_object('errorLogin')
        self.login = self.builder.get_object('Login')
        self.quit = self.builder.get_object('quit')
	
        #dns window
        #
        self.window_dns = self.builder.get_object('dnsWindow')
        self.menubar_dns = self.builder.get_object('menubar1')
        self.comboBox_dns = self.builder.get_object('comboboxtext1')        
        self.spinner = self.builder.get_object('spinner2')       
        self.start_chat_button = self.builder.get_object('start_Chat')
        self.update_dns_button = self.builder.get_object('update_dns')
        self.error_dns_textbox = self.builder.get_object('errorDns')   

        #chat box
        #
        self.window_chatbox = self.builder.get_object('chatBox')
        self.scrollDisplay_chatbox = self.builder.get_object('scrollDisplay')
        self.viewDisplay_chatbox = self.builder.get_object('viewDisplay')
        self.enterMessage_chatbox = self.builder.get_object('enterMessage')
        self.textView_chatbox = self.builder.get_object('textView')
        self.sendMessage_button = self.builder.get_object('sendMessage')
        
        #model to create strings for the combo box
        #will be filled later
        #
        self.dns_chatters = Gtk.ListStore(str)
          
        #close program if windows below are destroyed, they can still be hidden
        # 
        if(self.login_window):
            self.login_window.connect('destroy',Gtk.main_quit)
        if(self.window_dns):
            self.window_dns.connect('destroy',Gtk.main_quit)
          
        #connect objects that have reactions to functions defined later in class
        #
        self.dic = {
            "on_Login_clicked" : self.loginClick,
            "on_quit_clicked" : self.quitClick,
            #"on_comboboxtext1_changed" : self.comboChanged,
            "on_start_Chat_clicked" : self.startChatClick,
            "on_update_dns_clicked" : self.updateDns,
            "on_sendMessage_clicked" : self.sendMessageClick
        }  
    
        self.builder.connect_signals(self.dic)

        #show login window
        #
        self.login_window.show()
        
         
    
    # -- START FUNCTION DESCRIPTION --
    #
    # login button clicked
    # grab username, password, and misc information
    # check if given information is valid
    # start DNS window 
    # start thread to run backround information
    # 
    # -- END FUNCTION DESCRIPTION --
    def loginClick(self,widget):
        
        #Get text from the user
        #
        callSign = self.userName.get_text()
        self.routerPassword = self.passWord.get_text()
        miscInformation = self.miscellaneous.get_text()

        #Check if information is valid
        #
        if not self.routerPassword:
            self.errorMessage.set_text('No Password Entered')
        
        elif not callSign:
            self.errorMessage.set_text('No Username Entered')
        
        #Start toiChatclient
        #
        else:
            if not miscInformation:
                self.myToiChatClient = toiChatClient(callSign)
            else:
                self.myToiChatClient = toiChatClient(callSign,miscInformation)
            #Verify if password given is correct
            #
            try: 
                self.verified_routerPassword = testSSH(self.routerPassword)
            except Exception as e:
                self.errorMessage.set_text(str(e))
                return
  
            #All information needed is set, open next window
            # 
            self.login_window.hide() 
            self.window_dns.show()
             
            #start the spinner 
            #can't block from here on out or spinner won't update
            #
            self.spinner.start()

            #create thread to start server when the spinner is spinning
            #
            start_ToiChat_thread = threading.Thread(target=self.startToiChat)
            start_ToiChat_thread.daemon = True
            start_ToiChat_thread.start()
        
    # -- START FUNCTION DESCRIPTION --
    #
    # Start the server and do a forcednsupdate
    # This must be threaded as it executes blocking operations 
    # populate combo box with current dns 
    #
    # -- END FUNCTION DESCRIPTION --
    def startToiChat(self):
        #intstantiate major backbone objects that wil handle chatting
        #
        self.myNameServer = toiChatNameServer(self.myToiChatClient,self.verified_routerPassword)
        self.myToiChatClient.updateNameServer(self.myNameServer)
        self.myToiChatServer = toiChatServer(self.myNameServer)
        self.myToiChatServer.startServer()
        
        #attempt to connect to a server, if unsuccessful exit program
        #
        if self.myNameServer.attemptFindServer() == True:
            print('sucess')
        else:
            self.error_dns_textbox.set_text('Connection to ToiChat Network Failed. Please Try again in a few minutes')
       
        #get clients
        #this needs to be in a while loop because it can take away for the client list to populate
        #
        self.clientList = [];      
        while(self.clientList == []):
            #try:
            self.clientList = self.myNameServer.getClients()
            #except Exception as e:
            #     self.error_dns_textbox.set_text('Error finding Clients. Please try again')
 
        #add clients to liststore object attached to comboBox 
        #
        for client in self.clientList:
            self.dns_chatters.append([str(client)])
       
        #display clients in the gui
        #
        self.comboBox_dns.set_model(self.dns_chatters)              
        
        #operation complete stop spinner
        #
        self.spinner.stop()

    # -- START FUNCTION DESCRIPTION --
    # 
    # on Start Chat button clicked grab the name from the combo box
    # and start a chat 
    #
    # -- END FUNCTION DESCRIPTION --     
    def startChatClick(self, widget):
        #retrieve current selection from combo box
        #
        chatter = self.comboBox_dns.get_active_text()
        
        #check to see if user actually selected an entry or if box is empty
        #
        if(chatter ==  None):
            self.error_dns_textbox.set_text('Nothing Selected. Select a Name to Continue.')
        else:
            self.chatBox(chatter)   

    # -- START FUNCTION DESCRIPTION -- 
    #
    # Intiate chat with valid user
    # Open instance of chat window 
    # grab text to send to other chatter
    # recieve text and put it in viewable area 
    #
    # -- END FUNCTION DESCRIPTION --
    def chatBox(self,current_chatter):
        print(current_chatter)
        self.window_chatbox.show() 
        buffer = self.textView_chatbox.get_buffer()
        buffer.set_text('test')
        self.textView_chatbox.set_buffer(buffer)
    
    # -- START FUNCTION DESCRIPTION --
    #
    # function to handle 'Send Message' button clicks
    # grabs text inputed 
    #
    # -- END FUNCTION DESCRIPTION -- 
    def sendMessageClick(self, widget):
        newMessage = self.enterMessage_chatbox.get_text()
        if not newMessage:
            self.error_dns_textbox.set_text('No Message Entered.')
        print(newMessage)
        self.displayMessageSent(newMessage)
 
    def displayMessageSent(self, message):
        print('displayMessageSent')
        print(newMessage)

    # -- START FUNCTION DESCRIPTION -- 
    #
    # when update chatters button is clicked,
    # this function starts and starts a spinner to indicate program is working 
    # calls another function in thread so spinner can work while background operations are running
    #
    # -- END FUNCTION DESCRIPTION --
    def updateDns(self, widget):
        #start the spinner
        #
        self.spinner.start()
        
        #start a thread to update dns so the operation will not block spinner
        #
        start_Update_Dns_thread = threading.Thread(target=self.threadUpdateDns)
        start_Update_Dns_thread.daemon = True
        start_Update_Dns_thread.start()
    
    # -- START FUNCTION DESCRIPTION --
    # 
    # in this thread the DNS is updated 
    # gui is also graphically updated
    # ListStore must be cleared beforehand or some names will be duplicated
    # 
    # -- END FUNCTION DESCRIPTION --  
    def threadUpdateDns(self):
        print('threadUpdateDns')
        if self.myNameServer.attemptFindServer() == True:
            print('conn success')
        else:
            self.error_dns_textbox.set_text('Connection to ToiChat Network Failed. Please Try Again Later')
        
        self.clientList = []
        while(self.clientList == []):
             self.clientList = self.myNameServer.getClients()

        self.dns_chatters.clear() 

        for client in self.clientList:
            self.dns_chatters.append([str(client)])

        self.comboBox_dns.set_model(self.dns_chatters)

        self.spinner.stop()

    # -- START FUNCTION DESCRIPTION --
    #
    # quit program if quit is presed on login screen
    #
    # -- END FUNCTION DESCRIPTION --    
    def quitClick(self, widget):
        sys.exit(0)

# -- MAIN --
#
# intialize threading
# start gui 
# wait in main loop to recieve interrupts or signals
#
if __name__ == "__main__":
    GObject.threads_init()
    toichatGui = ToiChatGui()
    Gtk.main()  
