# Import Modules
import os, sys
import subprocess
from modules.gatewayIP import gatewayIP
def listen_router():
    # Find the default gateway
    # 
    default_gateway = gatewayIP()
    print (default_gateway)
    # Find directory with router scripts
    #
    # scriptPath = os.path.join(os.path.join( \
    #    os.path.dirname(os.path.dirname(os.path.dirname( \
    #    os.path.dirname(os.path.dirname(
    #    os.path.abspath(__file__)))))), \
    #    "router-scripts"), \
    #    'router_tx_arpinfo.sh')
    scriptPath = "../etc/router_tx_arpinfo.sh"
    # Run '../router-scripts/router_tx_arpinf.sh' on local router
    #
    ssh = subprocess.Popen(['ssh', '-p', '2222', \
        'root@' + default_gateway, "'sh '" + scriptPath], \
        shell=False, \
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

