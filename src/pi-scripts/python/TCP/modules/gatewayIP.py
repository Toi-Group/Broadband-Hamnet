#!/usr/bin/env python3

import subprocess


# -- START FUNCTION DESCR --
#
# Example Usage:
#   - routerIP = gatewayIP()
# Get IP of default gateway 
# Inputs:
#   None
# Outputs:
#   - routerIP = IP of local router connected to machine
#
# -- END FUNCTION DESCR -- 
def gatewayIP():

    cmd = "route -n | grep 'UG'"
    route = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    routerIP = route.communicate()[0]
    routerIP = str(routerIP).split()
    print("Default Gateway Found: \n\t" + routerIP[1])
    return routerIP[1]


