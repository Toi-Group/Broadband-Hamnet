#!/usr/bin/env python3

# Function gatewayIP.py
# example use - routerIP = gatewayIP()
# get IP of router connected to local machine
# output - routerIP - IP of local router connected to machine
#
import subprocess

def gatewayIP():

    cmd = "route -n | grep 'UG'"
    route = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    routerIP = route.communicate()[0]
    routerIP = str(routerIP).split()
    print(routerIP[1])
    return routerIP[1]

