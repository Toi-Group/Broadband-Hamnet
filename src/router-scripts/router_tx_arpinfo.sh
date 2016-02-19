#!/bin/bash

# Define port toi-chat uses to communicate between routers
#
toiPort=5005
toiPort2=5006

# Ensure no netcat ports are currently listening
#

# Grep for the netcat port
#
found="$(ps | grep '[n]c -lp 5005 | wc -l')"

# Did the process exist?
#


if [ $found -eq 1 ]
then
    #if the process existed, get the PID and kill the process
    #
    grep_out="$(ps | grep '[n]c -lp 5005')"
    proc_ID="$(echo $grep_out | awk '{print $1;}')"
    kill -9 $proc_ID
    echo "Killed Process" $proc_ID
fi

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
        arp -i eth0.0 | grep -oE '\(([^)]+)\)' | tr -d '()' | nc $rx_IP $toiPort2
done
