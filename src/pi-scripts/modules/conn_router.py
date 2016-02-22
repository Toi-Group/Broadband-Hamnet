
#!/usr/bin/env python3

import os # Used for testing the location to the router script is valid
import socket # Used for testing IP validity.
import subprocess # Used for running shell commands

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
def conn_router(default_gateway, user_pwd):
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
    ssh = subprocess.Popen(['sshpass', '-p', user_pwd, \
        'ssh', '-p', '2222', \
        'root@' + default_gateway,'sh ' + scriptPath], \
        shell=False, \
        stdout=subprocess.PIPE, \
        stderr=subprocess.PIPE)
 
    # Take output of command and return. 
    #
    nodes = ssh.communicate()[0]
    if len(nodes) < 7:
        # error = ssh.stderr.readlines()
        return None 
    else:
        #Parse output to extract IPs of local machines
        #
        IPs = nodes.decode('ascii').split('\\n')

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
    #Return a list of IPs found on the mesh network
    #
    return valid_IPs

