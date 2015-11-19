
##--- Title: parse_order.py
##--- Description: Parses a text file, or string, and numbers
##---              them according to the desired packet size
##--- Author: Robert Irwin


##---IMPORTANT: Every time you run this, delete dump.txt
import sys
import math

#file = open("sample_parse.txt", "r")
#message = str(file.read())

#debugging case comment out the line below this and uncomment the two lines 
#above this to test on a large file.  sample_parse.txt is on Github as well

message = "Hello World. I have a whole lot of friends!"
def parse_order(message):
    count = 1
    dump = open("dump.txt", "a")
    temp = [];
    #this is the packet size
    packet = 5;

    #determine how many packets we will need
    length = len(message)


    #now we must determine the size of our max order number
    test = 1
    maxnum = int(math.ceil(length/(packet-test)))

    while len(str(maxnum)) > len(str(test)):
        test += 1
        if len(str(test)) > 2:
            print('Error: Message too large')
    #the max number of digits we will have to apend to each packet is
    #equal to the number of digits in test!
    ordlen = len(str(test))

    #determine how long to extend for loop to ensure that the entire message is parsed
    num_parse = int(math.ceil(length/(packet-ordlen))) #we want to round the division up to the nearset integer
                                                     #rememeber we are parsing by one less than the packet length 
                                                     #to leave room for the ordering 

# This section is still in the works.  I want to figure out the logic to make this work                                                             
#    for any size file.  Right now we can only effectively order 10 packets [0-10].  It will look like it works when looking at the .txt file
#    but the packets will start leaking into eachother because of size.  (we declared a size of 512 but when we append a 10, that packet should be 513) 
    for i in range(0,(packet)*num_parse,packet):
        if i == 0:
            temp[0:packet-1] = list(message[i:count*packet-1])
        else:
            temp[0:packet-1] = list(message[(i-2*(count-1))+count-1:(count*packet)-2*(count-1)+(count-2)])
#        print('count = ', count)

#BEGIN DEBUGGING SECTION FOR INDEXING THE MESSAGE

#        print('i=',i)
#        print('count=',count)
#        print('message goes from', (i-2*(count-1))+count-1, (count*packet)-2*(count-1)+(count-2)) 

#END DEBUGGING SECTION FOR INDEXING THE MESSAGE
#make sure were appending numbers on the end for no reason
        
        count = count + 1   # increment and check count against numparse of packets to ensure we arent wrting extra numbers to the file
        if count <= num_parse: #plus 1 because we increment before we check.  Without this the last packet doesnt get written
#now we start manipulating the data...

            temp1 = ''.join(temp) #change list to string
#            print(temp1)
            dump.write(temp1) #write the string to the dummy file
                              #it is important to note we are in append mode

            dump.write(str(count-1)) # subtract 1 because we increment count before we write to the file

#now that we are passed the max number of packets, we can stop
        else:
            dump.close()
            dump = open("dump.txt", "r")
            messtosend = dump.read()
            return(str(messtosend))
        

messtosend = parse_order(message)
print(messtosend)


## -I still dont have when to stop parsing figured out... Im still going over the desired amount,
#which is eveident by the string of numbers at the end of the message.
# -Also, I still have to include something that deletes dump.txt after it is read into messtosend
#so we dont have to keep deleting it manually after every run. 
