#!/bin/bash

# Define port toi-chat uses to communicate between routers
#
toiPort=5005

# Find the IP address of the local router
#
myIP="$(ifconfig | grep -A 8 eth0.0 | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*')"

# Construct message to send to other routers
#
sendMsg="toi-chatTx myIP=($myIP)"

# Get a list of all mesh-nodes local router can see and request information
# from them over what devices are connected to them.
#
for i in $( arp -i wl0 | grep -oE '\(([^)]+)\)' | tr -d '()' );
do
    echo $sendMsg | nc $i $toiPort
        rx="$(nc -lp $toiPort)"
    echo $rx
done
