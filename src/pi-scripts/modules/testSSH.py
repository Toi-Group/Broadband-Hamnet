#!/usr/bin/env python3

from modules.gatewayIP import gatewayIP
from subprocess import call

def testSSH():
    
    #find the default gateway
    #
    default_gateway = gatewayIP()

    rtrn = 7
 
    while(rtrn != 0):
        # prompt user for password
        #
        user_pwd = input("Router Password: ")

        # save to a file for sshpass  
        #
        with open("user_pwd.txt", "wt") as f:
            f.write(user_pwd)

        # validate the password
        #
        rtrn = call(['sshpass', '-p', user_pwd, \
            'ssh', '-p', '2222', \
            'root@' + default_gateway, "exit"]) 

        if ( rtrn == 5 ):
            print("Authentication Failed. Re-enter Password for Router.\n")

        elif ( rtrn == 6 ):
            print("RSA Fingerprint not verified. Please Try Again.")
            rtrn = call(['ssh', '-p', '2222', 'root@' +default_gateway, "exit 1"])

    return (user_pwd)
