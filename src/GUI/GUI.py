## needed headers
from tkinter import *
from tkinter import ttk
import socket
import sys
import time
import tkinter.scrolledtext as ScrolledText

#function definitions

def quit():
    #code to quit
    mainframe.quit()

##----------------------##
##------END QUIT()------##
##----------------------##

def send(*args):
    MESSAGE_success.set('')
    err_IP.set('')
    while True:
        UDP_IP = IP.get() #This gets the IP address from the GUI 
        try:
            socket.inet_aton(UDP_IP)  #converts a dot format IPv4 address to a 32-bit packed binary format
            # Legal
            break
        except socket.error: #if an invalid IPv4 address is entered, socket.error will be one due to socket.inet_aton
            # Not Legal
            err_IP.set("You need to enter a valid IPv4 address!")
            return None

# Prompt for PORT. Default 65104 if null input                                  
#                                                                               
    while True:
        try:
            err_PORT.set('')
            UDP_PORT = int(PORT.get())  #grabs the PORT number from the GUI.  Maybe enter a static PORT for user's ease???
        #        "(Default. 65104) >> ") or '65104')
        except ValueError:
            #print("You need to type in a valid PORT number!")
            err_PORT.set("You need to enter a valid PORT number!")
            return None
        else:
            if UDP_PORT in range(65535):
                break
            else:
                err_PORT.set("Port must be in range 0-65535!")
                return None

        

# Bind the socket                                                               
#                                                                               
# Send over internet using UDP                                                  
#                                                                               
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Run the program forever                                                       
    while True:
    # Prompt the user for a keystroke or message to send                        
    #                                                                           
        INFO = MESSAGE_entry.get("1.0", "end")

    # Send the message using the socket opened                                  
    #                                                                           
        sock.sendto(bytes(INFO, 'UTF-8'), (UDP_IP, UDP_PORT))

    # Confirm with the user  the message sent succesfully                        
    #                                                                           
    # ##----OLD CONFIRMATION MESSAGE----##
    #    MESSAGE_success.set("Seccessfully sent message: {}" .format(str(INFO)))
        MESSAGE_success.set("Message Sent Successfully")
        return None

## -------------------------------- ##
## -------------------------------- ##
## -------------------------------- ##
## -----------END SEND()----------- ##
## -------------------------------- ##                                         
## -------------------------------- ##
## -------------------------------- ## 

#Begin formatting the GUI
root = Tk()
root.title("TOI Communication: Send")

mainframe = ttk.Frame(root, padding="120 120 120 120")
mainframe.grid(column=0, row =0, sticky=(N,W,E,S))
mainframe.rowconfigure(0, weight = 1)
mainframe.columnconfigure(0, weight = 1)

#define variables
IP = StringVar()
err_IP = StringVar()
MESSAGE = StringVar()
MESSAGE_success = StringVar()
#MESSAGE_send = StringVar()
PORT = StringVar()
err_PORT = StringVar()

#Get necessary variables and place text boxes on the grid
IP_entry = ttk.Entry(mainframe, width = 18, textvariable = IP)
IP_entry.grid(column = 2, row = 1)

PORT_entry = ttk.Entry(mainframe, width = 7, textvariable = PORT)
PORT_entry.grid(column = 2, row = 2)

##----THIS WAS ORIGINAL MESSAGE ENTRY WIDGET----##
#MESSAGE_entry = ttk.Entry(mainframe, width = 25, textvariable = MESSAGE)
#MESSAGE_entry.grid(column = 2, row = 3)


#this is the scroll box
MESSAGE_entry = ScrolledText.ScrolledText(mainframe, height = 0, width = 30,
    borderwidth=0, padx = 0)
MESSAGE_entry.grid(column = 2, row = 3)
MESSAGE_entry.configure(highlightbackground="grey", highlightcolor="grey", borderwidth = 0)

ttk.Label(mainframe, text = "Enter IP Address").grid(column = 1, row = 1)
ttk.Label(mainframe, text = "Enter the PORT for Communication").grid(column = 1, row = 2)
ttk.Label(mainframe, text = "Enter the Message").grid(column = 1, row = 3)
ttk.Button(mainframe, text = "Send", command = send).grid(column = 4, row = 4)
ttk.Button(mainframe, text = "Quit", command = quit).grid(column = 1, row = 4)
ttk.Label(mainframe, textvariable=err_IP, foreground='red').grid(column=3, row=1)
ttk.Label(mainframe, textvariable=err_PORT, foreground='red').grid(column=3, row = 2)
ttk.Label(mainframe, textvariable=MESSAGE_success, wraplength = 400).grid(column = 2, row = 4)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

IP_entry.focus()
PORT_entry.focus()
MESSAGE_entry.focus()
root.bind('<Return>', send)

#run it
MESSAGE_success.set('')

root.mainloop()
