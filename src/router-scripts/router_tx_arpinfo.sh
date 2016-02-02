#!/bin/sh

# Define port toi-chat uses to communicate between routers
#
toiPort=5005

# Loop forever (always be listening)
while [ 1 ]
do
    # Start listening to traffic over network specifically port 5010
    #

    rx_mess="$(nc -lp $toiPort)"
    
    # Debug print send message
    #
    echo $rx_mess

    # Check if message is from TOI-Chat
    #
    val="$(echo $rx_mess | grep "toi-chatTx" | wc -l)"
    if [ $val = 1 ]
    then
        # Find the IP of the requesting router
        #
        rx_IP="$(echo $rx_mess | grep -oE '\(([^)]+)\)' | tr -d '()')"
        
        # Output this routers ARP table to the requesting router
        #
        arp -i eth0.0 | grep -oE '\(([^)]+)\)' | tr -d '()' | nc $rx_IP $toiPort
done
