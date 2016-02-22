# Import Modules
import os, sys
import subprocess
from modules.gatewayIP import gatewayIP


def listen_router(user_pwd):
    # Find the default gateway
    # 
    default_gateway = gatewayIP()

    scriptPath = "../etc/router_tx_arpinfo.sh &"

    # Run '../router-scripts/router_tx_arpinf.sh' on local router
    #
    ssh = subprocess.Popen(['sshpass', '-p', user_pwd, \
        'ssh', '-p', '2222', \
        'root@' + default_gateway, "sh "  + scriptPath], \
        shell=False, \
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

