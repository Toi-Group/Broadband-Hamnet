#!/usr/bin/env python3

from modules.gatewayIP import gatewayIP
from subprocess import call
import getpass

def testSSH(user_pwd):
    
    #find the default gateway
    #
    default_gateway = gatewayIP()

    rtrn = 7
 
    while(rtrn != 0):
        
        #if not user_pwd:
            # prompt user for password
            #
            #print('why you here')
            #user_pwd = getpass.getpass("\nRouter Password >> ")

        # save to a file for sshpass  
        #
        #with open("user_pwd.txt", "wt") as f:
        #    f.write(user_pwd)

        # validate the password
        #
        rtrn = call(['sshpass', '-p', user_pwd, \
            'ssh', '-p', '2222', \
            'root@' + default_gateway, "exit"]) 

        if ( rtrn == 5 ):
            raise Exception("Authentication Failed. Re-enter Password for Router.")

        elif ( rtrn == 6 ):
            rtrn = call(['ssh', '-p', '2222', 'root@' +default_gateway, "exit 1"])
            raise Exception("RSA Fingerprint not verified")

    return (user_pwd)
