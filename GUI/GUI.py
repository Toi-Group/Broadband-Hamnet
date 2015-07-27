## needed headers
from tkinter import *
from tkinter import ttk
import socket

#function definitions

def quit():
    #code to quit
    mainframe.quit()

##----------------------##
##------END QUIT()------##
##----------------------##

def send(*args):
    #send_udp code                                                                
    # Source: https://wiki.python.org/moin/UdpCommunication                         # This code sends a message to another script running at the UDP_IP destination
    # the script receive_udp.py                                                     # Get local IP                                                                  #localIP = socket.gethostbyname(socket.gethostname())
    # Setup connection to other Pi                                                  # Prompt for IP. Default localIP if null input 
    while True:
#        print ("Enter the IP of the client machine you will be "
#            "communicating with. (Default Local IP: '{}')"
#            .format(str(localIP)), end="")
        ##UDP_IP = input(" >> ") or localIP
        UDP_IP = IP.get()
        try:
            socket.inet_aton(UDP_IP)
            # Legal
            break
        except socket.error:
            # Not Legal                                                             
            print("You need to enter a valid IPv4 address!\n")
            continue

# Prompt for PORT. Default 65104 if null input                                  
#                                                                               
    while True:
        try:
            #UDP_PORT = int(input("Enter the PORT you will be communicating over. "
            UDP_PORT = int(PORT.get())

        #        "(Default. 65104) >> ") or '65104')
        except ValueError:
            print("You need to type in a valid PORT number!")
            continue
        else:
            if UDP_PORT in range(65535):
                break
            else:
                print("Port must be in range 0-65535!")
                continue
# Bind the socket                                                               
#                                                                               
# Send over internet using UDP                                                  
#                                                                               
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Run the program forever                                                       
    while True:
    # Prompt the user for a keystroke or message to send                        
    #                                                                           
        #MESSAGE = input("What would you like to send (keyboard input)>> ")
        INFO = MESSAGE.get()

    # Let the user know what IP and Port we are using to communicate with       
    #                                                                           
        print ('Sending message to UDP target: {}:{}' .format(str(UDP_IP),
            UDP_PORT))

    # Send the message using the socket opened                                  
    #                                                                           
        sock.sendto(bytes(INFO, 'UTF-8'), (UDP_IP, UDP_PORT))

    # Confirm with the user the message sent succesfully                        
    #                                                                           
        print ("Successfully sent message: {}" .format(str(INFO)))

## -------------------------------- ##
## -------------------------------- ##
## -------------------------------- ##
## -----------END SEND()----------- ##
## -------------------------------- ##                                         
## -------------------------------- ##                                          ## -------------------------------- ## 

#Begin formatting the GUI
root = Tk()
root.title("Preparation for Communication")

mainframe = ttk.Frame(root, padding="120 120 120 120")
mainframe.grid(column=0, row =0, sticky=(N,W,E,S))
mainframe.rowconfigure(0, weight = 1)
mainframe.columnconfigure(0, weight = 1)

#define variables
IP = StringVar()
MESSAGE = StringVar()
PORT = StringVar()

#Get necessary variables and place text boxes on the grid
IP_entry = ttk.Entry(mainframe, width = 18, textvariable = IP)
IP_entry.grid(column = 3, row = 1)

PORT_entry = ttk.Entry(mainframe, width = 7, textvariable = PORT)
PORT_entry.grid(column = 3, row = 2)

MESSAGE_entry = ttk.Entry(mainframe, width = 25, textvariable = MESSAGE)
MESSAGE_entry.grid(column = 3, row = 3)

ttk.Label(mainframe, text = "Enter IP Address").grid(column = 1, row = 1)
ttk.Label(mainframe, text = "Enter the PORT for Communication").grid(column = 1, row = 2)
ttk.Label(mainframe, text = "Enter the Message").grid(column = 1, row = 3)
ttk.Button(mainframe, text = "Send", command = send).grid(column = 4, row = 4)
ttk.Button(mainframe, text = "Quit", command = quit).grid(column = 1, row = 4)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

IP_entry.focus()
PORT_entry.focus()
MESSAGE_entry.focus()
root.bind('<Return>', send)

#run it
root.mainloop()
