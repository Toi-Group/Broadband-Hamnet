#!/usr/bin/env python

import commands

#localIP
#returns first listed IPv4 "inet addr", usually eth0
def localIP():
    
    #run unix command to parse ifconfig for inet addr
    #
    ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | grep -iv \"inet6\" | " + "awk {'print $2'} | sed -ne 's/addr\:/ /p'")
    
    #ips now contains all inet addr, one is etho0 and the other is lo
    #we don't want lo (127.0.0.1) so we make ips the only relevant IP
    #
    ips = ips.split()[0]
    
    #end gracefully
    #
    return ips

#testing purposes
#def main():
    
    #IP =localIP()
    #print(IP)

#if __name__ == '__main__':
    #main()

