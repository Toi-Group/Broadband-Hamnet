
#!/usr/bin/env python3

import os # Used for testing the location to the router script is valid
import socket # Used for testing IP validity.
import subprocess # Used for running shell commands
import re # Used for parsing ping result

# -- START FUNCTION DESCR --
#
# This program establishes a connection to a broadband-hamnet
# router and runs '../router-scripts/router_request_arpinf.sh'.
#
# Inputs:
#  - default_gateway = the default gateway address which the mesh can be 
#       found
#
# Outputs:
#  - IPs = returns the IPv4 addresses of nodes found on the mesh network in a list.
#
# -- END FUNCTION DESCR -- 
def conn_router(default_gateway):
    # Directory with router scripts
    #
    scriptPath = 'router_request_arpinfo.sh'

    # Try to open 'router_request_arpinf.sh'
    #
    #if (os.path.isfile(scriptPath) == False):
        #print('There was an error opening the file \''+scriptPath+'\'')
        #sys.exit(1)

    # Construct ssh command to run 'router_request_arpinf.sh' script
    #
    ssh = subprocess.Popen(['ssh', '-p', '2222', \
        'root@' + default_gateway,'sh ' + scriptPath], \
        shell=False, \
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
 
    # Take output of command and return. 
    #
    nodes = ssh.communicate()[0]
    if len(nodes) < 7:
        error = ssh.stderr.readlines()
        return None 
    else:
        #Parse output to extract IPs of local machines
        #
        nodes = str(nodes).split('\\n')
        IPs = str(nodes[1]).split()

        # Check if IPs are valid IPv4 addresses
        #
        valid_IPs = []
        for TCP_IP in IPs:
            try:
                socket.inet_aton(TCP_IP)
            except socket.error:
                pass
            # If valid add it to the array
            #
            valid_IPs.append(TCP_IP)
        # Check if we have any valid IPs. Return None if we don't
        #
        if valid_IPs == []:
            return None
    #valid_IPs = pingIPSort(valid_IPs)
    
    #Return a list of IPs found on the mesh network
    #
    return valid_IPs

# Pings a list of IPs. 
# 
# Input:
# - List of IPs
#
# Output: 
# - a list of IPs sorted by lowest ping time. Also removes any 
#       results that resulted in no response
#
def pingIPSort(listIPs):
    pingResult = []
    # We now have a list of IPs. We sort them by fastest ping
    #
    for IP in listIPs:
        # We now have a list of IPs. We sort them by fastest ping
        #
        try:
            ping = subprocess.Popen(["ping","-c 5", IP], \
                stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
            out, error = ping.communicate()
            print("Out = " + str(out))
            if out:
                try:
                    average = int(re.findall(r"/(\d+)/", out)[1])
                    pingResult.append(average)
                except:
                    listIPs.remove(IP)
            else:
                # No ping result. Remove from list
                #
                listIPs.remove(IP)
        except subprocess.CalledProcessError:
            listIPs.remove(IP)
        

    print("averages = " + str(pingResult))
    listIPs = [listIPs for (pingResult,listIPs) in \
            sorted(zip(pingResult,listIPs), key=lambda pair: pair[0])]
    return listIPs