#!/usr/bin/env python3

# This program establishes a connection to a broadband-hamnet
# router and runs '../router-scripts/router_request_arpinf.sh'.

# Inputs:
#  - default_gateway = the default gateway address which the mesh can be 
#       found

# Outputs:
#  - nodes = returns the IPv4 addresses of nodes found on the mesh network.

# Import Modules
import os, sys
import subprocess

def conn_router(default_gateway):
    # Find directory with router scripts
    #
    scriptPath = os.path.join(os.path.join( \
        os.path.dirname(os.path.dirname(os.path.dirname( \
        os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))), \
        "router-scripts"), \
        'router_request_arpinfo.sh')

    # Try to open 'router_request_arpinf.sh'
    #
    if (os.path.isfile(scriptPath) == False):
        print('There was an error opening the file \''+scriptPath+'\'')
        sys.exit(1)

    # Construct ssh command to run 'router_request_arpinf.sh' script
    #command_line = "ssh -p 2222 root@" + default_gateway + \
    #    " 'sh' < " + scriptPath
    
    # Run '../router-scripts/router_request_arpinf.sh' on local router
    #
    print(scriptPath)
    # ssh = subprocess.Popen(['ssh', '-p', '2222', \
    #     'root@' + default_gateway, "'sh'", "<", scriptPath], \
    #     shell=True,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE)
    ssh = subprocess.Popen(['ssh', '-p', '2222', \
        'root@' + default_gateway, "'sh < '" + scriptPath], \
        shell=False, \
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    ssh.wait()

    # Take output of command and return
    #
    nodes = ssh.communicate()[0]
    if nodes == "":
        error = ssh.stderr.readlines()
        print("error")
        print(error)
    else:
        print("success")
        print(nodes)
    # Return a list of nodes found on the mesh network
    #
    exit(1)
    return nodes