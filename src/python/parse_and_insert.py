import math
import sys

#file = open("sample_parse.txt", "r")
#message = str(file.read())
message = "Hello World.  I have a whole lot of friends!"
def parse(message):
    count = 1
    dump = open("dump.txt", "a")
    temp = [];
    #this is the packet size
    packet = 3;
    print(len(message))
    for i in range(0,len(message),packet):
        #dump = open("dump.txt", "a")
#        print(str(count))
        if i == 0: 
            temp[0:packet-2] = list(message[i:count*packet-2])
        else:
            temp[0:packet-2] = list(message[i-1:count*packet-2])
        print(i)
            #define a temp string
#        temp = ''.join(temp)
#        temp1 = ''.join(temp)
        temp1 = str(temp)
        print(temp1)
        dump.write(temp1)
        dump.write(str(count))
        count = count+1
    dump.close()
    dump = open("dump.txt", "r")
    messtosend = str(dump.read())
    return messtosend

messtosend = parse(message)
#print(messtosend)
