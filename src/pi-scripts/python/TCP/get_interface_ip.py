#!/usr/bin/env python3

#get IP of router connected to local machine
#

import os 
import socket
import struct
import fcntl

def main():

   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   print(socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth0'[:15]))[20:24]))


if __name__ == '__main__':
   main()

