from tkinter import *
from tkinter import ttk
import socket
import sys
import tkinter.scrolledtext as ScrolledText


#function definitions                                                                        

def quit():
    #code to quit 
    
    mainframe.quit()

##----------------------##
##-------END QUIT-------##
##----------------------##

def receive():
    err_IP.set('')
    status.set('')
    while True:
        UDP_IP = IP.get()
        try:
            socket.inet_aton(UDP_IP)
            # Legal                                           
            break
        except socket.error:
            # Not Legal   
            err_IP.set("You need to enter a valid IPv4 address!\n")
            return None

    # Prompt for PORT. Default 65104 if null input
    while True:
        try:
            err_PORT.set('')
            UDP_PORT = int(PORT.get())
        except ValueError:
            # Not Legal  
            err_PORT.set("You need to type in a valid PORT number!")
            return None
        else:
            if UDP_PORT in range(65535):
            # Not Legal
                break
            else:
                print("Port must be in range 0-65535!")
                # Legal 
                return None

        # Bind the socket
 
        # Receive over internet using UDP

    sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    # Prompt user we are now monitoring for messages#
   # print("Program is now monitoring {}:{} for messages" .format(str(UDP_IP),
   # UDP_PORT))
    while True:
#        print ("Waiting for Message")
        status.set('Waiting for Message...')
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data =  bytes.decode(data, 'UTF-8')

#        print ("received message: {}" .format(data))
        MESSAGE_entry.insert('1.0', data)
        MESSAGE_entry.insert('1.0', '/n-----------------------/n')
        status.set('Message Received')
##---------------------------------##
##---------------------------------##
##---------------------------------##
##-----------END RECEIVE-----------##
##---------------------------------##
##---------------------------------##
##---------------------------------##


#Begin Formatting the GUI
root = Tk()
root.title('TOI Communication: Receive')
mainframe = ttk.Frame(root, padding = "120 120 120 120")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
mainframe.rowconfigure(0, weight = 1)
mainframe.columnconfigure(0, weight = 1)

#define variable
IP = StringVar()
err_IP = StringVar()
PORT = StringVar()
err_PORT = StringVar()
status = StringVar()

#Get necessary variables and place text boxes on the grid
IP_entry = ttk.Entry(mainframe, width = 18, textvariable = IP)
IP_entry.grid(column = 2, row = 1)

PORT_entry = ttk.Entry(mainframe, width = 7, textvariable = PORT)
PORT_entry.grid(column = 2, row = 2)


ttk.Label(mainframe, text = "Enter IP Address of Sender").grid(column = 1, row = 1)
ttk.Label(mainframe, text = "Enter PORT for Communication").grid(column = 1, row = 2)
ttk.Label(mainframe, text = "Message").grid(column = 1, row = 3)
ttk.Button(mainframe, text = "Wait", command = receive).grid(column = 4, row = 5)
ttk.Button(mainframe, text = "Quit", command = quit).grid(column = 1, row = 5)
ttk.Label(mainframe, textvariable=err_IP, foreground='red').grid(column=3, row=1)
ttk.Label(mainframe, textvariable=err_PORT, foreground='red').grid(column=3, row = 2)
ttk.Label(mainframe, textvariable=status).grid(column=2,row=3)

MESSAGE_entry = ScrolledText.ScrolledText(mainframe, height = 0, width = 30,
    borderwidth=0, padx = 0)
MESSAGE_entry.grid(column = 2, row = 3)
MESSAGE_entry.configure(highlightbackground="grey", highlightcolor="grey", borderwidth = 0)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

IP_entry.focus()
PORT_entry.focus()
root.bind('<Return>', receive)


#run it

root.mainloop()
