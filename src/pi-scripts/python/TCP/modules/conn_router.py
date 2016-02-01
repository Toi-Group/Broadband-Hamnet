
#!/usr/bin/env python3

# This program establishes a connection to a broadband-hamnet
# router and runs '../router-scripts/router_request_arpinf.sh'.

# Inputs:
#  - default_gateway = the default gateway address which the mesh can be 
#       found

# Outputs:
#  - IPs = returns the IPv4 addresses of nodes found on the mesh network in a list.

# Import Modules
import os, sys
import subprocess

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
        'root@' + default_gateway,'sh '  + scriptPath], \
        shell=False, \
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
 
    # Take output of command and return
    #
    nodes = ssh.communicate()[0]
    if nodes == "":
        error = ssh.stderr.readlines()
        print("error")
        print(error)
    else:
        print("success")
  
    #Parse output to extract IPs of local machines
    #
    IP = str(nodes).split('\\n')
    IPs = str(IP[1]).split()
    print(IPs)

    #Return a list of IPs found on the mesh network
    #
    exit(1)
    return IPs
