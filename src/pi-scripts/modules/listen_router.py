# Import Modules
import os, sys
import subprocess
from gatewayIP import gatewayIP
#def listen_router():
def main():    
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
    # Try to open 'router_request_arpinf.sh'
    #
    if (os.path.isfile(scriptPath) == False):
        print('There was an error opening the file \''+scriptPath+'\'')
        sys.exit(1)

    # Construct ssh command to run 'router_tx_arpinf.sh' script
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
        'root@' + default_gateway, "'sh '" + scriptPath], \
        shell=False, \
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

if __name__ =='__main__':
    main()
