#!/usr/bin/env python3

# 
# Python toiChat Pinging Service
#  Class the enables handling ICMP handling to toiChatServers.
#
#
# Created on: 02/10/2016
# Author: Toi-Group
#

from modules.external.python_ping.ping import *
from collections import OrderedDict
# Pings a list of IPs. 
# 
# Input:
# - List of IPs
#
# Output: 
# - Tuple 1 : List of IPs sorted by lowest avg ping time.
# - Tuple 2: List of invalid IPs
#
def pingIPSort(listIPs, myCount=1):
    pingResult = {}
    invalidIPs = []
    sortedIPs = {}

    # We now have a list of IPs. We sort them by fastest ping
    #
    for destIP in listIPs:
        print("destIP = " + str(destIP))
        # We now have a list of IPs. We sort them by fastest ping
        #
        avgTime = quiet_ping(destIP, count=myCount)
        
        # Check to see if quient_ping return valid results
        #
        if (isinstance(avgTime, bool) == True) or avgTime == 0:
            invalidIPs.append(destIP)
            # We skip adding this IP to the dictionary
            #
            continue

        # We add the avgTime to a list containing average IPs
        #
        pingResult[destIP] = avgTime[2]

    # Compute the sorted dictionary if we have valid IPs
    #
    sortedIPs = OrderedDict(sorted(pingResult.items()))

    print(str(sortedIPs))
    return list(sortedIPs.keys()), invalidIPs