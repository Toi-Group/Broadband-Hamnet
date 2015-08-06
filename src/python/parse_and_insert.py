# !python3
##--- Title: parse_order.py
##--- Description: Parses a text file, or string, and numbers
##---              them according to the desired packet size
##--- Author: Robert Irwin

import sys, math, os

#file = open("sample_parse.txt", "r")
#message = str(file.read())

# Debugging case comment out the line below this and uncomment the two lines 
# Above this to test on a large file.  sample_parse.txt is on Github as well

def parse_order(message, packet_size):
# -----------------------------
# - DECLARE WORKING VARIABLES -
# -----------------------------

    f = open("_parse_tmp.txt", "a")
    packet_message = [];
    
    # Determine how many packets we will need
    length = len(message)

    # Now we must determine the size of our max order number
    test = 1
    maxnum = int(math.ceil(length/(packet_size-test)))

    while len(str(maxnum)) > len(str(test)):
        test += 1
        if len(str(test)) > 2:
            print('Error: Message too large')
    # The max number of digits we will have to append to each packet is
    # equal to the number of digits in test!
    ordlen = len(str(test))

    # Determine how long to extend for loop to ensure that the entire message is parsed
    # we want to round the division up to the nearset integer
    # remember we are parsing by one less than the packet length 
    # to leave room for the ordering 
    num_parse = int(math.ceil(length/(packet_size-ordlen)))
    
# -------------------------------------------------------
# - PARSE MESSAGE INTO PACKET SIZE & NUMBER THE PACKETS -
# -------------------------------------------------------
#   This section is still in the works.  I want to figure out the logic to make this work                                                             
#   for any size file.  Right now we can only effectively order 10 packets [0-10].  It will look like it works when looking at the .txt file
#   but the packets will start leaking into each other because of size.  (we declared a size of 512 but when we append a 10, that packet_size should be 513) 
    loop_count = 1
    for i in range(0,(packet_size)*num_parse,packet_size):
        packet_message = message[i:loop_count*packet_size]

# ----------------------------------------------------
# - BEGIN DEBUGGING SECTION FOR INDEXING THE MESSAGE -
# ----------------------------------------------------
        f.write("\n\n" +str(loop_count) + packet_message) 
        loop_count = loop_count + 1
    f.close()
    f = open("_parse_tmp.txt", "r")
    messtosend = f.read()
    f.close()
    os.remove('_parse_tmp.txt')
    return(str(messtosend))
    
# --------------------
# - Function Testing -
# --------------------
message = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque eget gravida nibh, ut condimentum ligula. Nam rutrum massa vitae lacus lobortis rutrum. Mauris pulvinar enim mauris, ut luctus ipsum dictum ac. Duis condimentum, velit sit amet efficitur ullamcorper, ex nisl accumsan lacus, et aliquam arcu neque at est. Sed pretium gravida bibendum. In dapibus rutrum lacus non pharetra. Pellentesque sem ipsum, varius ac purus id, vulputate dictum nisl. Nunc viverra libero sed mi euismod, vitae molestie metus bibendum. Suspendisse in nulla dui. "
	"Sed pharetra, orci sed congue rutrum, ipsum ante fermentum metus, eu pharetra est tellus at urna. Ut et est eu turpis viverra accumsan. Etiam eu malesuada quam. Nunc nulla massa, egestas vel imperdiet ut, fringilla et lectus. Sed vel dapibus sapien, at sagittis lacus. Donec sollicitudin mi sed dolor bibendum, scelerisque laoreet sapien euismod. Ut neque magna, dignissim eu augue sed, ultrices molestie diam. Mauris sit amet purus placerat, lobortis sem vitae, mattis nulla. Nunc lobortis, lacus in ultrices dignissim, eros orci imperdiet lectus, eget dignissim urna ipsum nec libero. Donec at bibendum odio. Vivamus nisi diam, luctus at packet_messageus non, sodales eget nunc. "
	"Donec mattis erat vestibulum pharetra auctor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nam viverra dolor turpis, vel auctor ligula finibus a. Nulla imperdiet nisi odio, ut vulputate ligula egestas et. Nulla congue lectus nec nulla malesuada tincidunt. Etiam scelerisque gravida egestas. In porta turpis magna, sed varius enim convallis a. Maecenas ut nisl a mi lacinia blandit. Vestibulum eu risus sit amet eros hendrerit efficitur in sit amet nisl. Nam venenatis, turpis sed gravida vehicula, sem tellus cursus nunc, vel sodales felis mauris vitae velit. Fusce ornare, nisl vel congue ullamcorper, ante ipsum vulputate enim, id vestibulum nisl odio quis libero. Suspendisse diam ligula, pulvinar sit amet augue eget, mollis laoreet neque. Suspendisse magna purus, tincidunt at nisi id, hendrerit congue leo. "
	"Nulla egestas, eros sed pellentesque dictum, mi erat suscipit sapien, vitae facilisis diam velit et velit. Ut mollis sed nulla ut viverra. Donec ultrices sem eu leo ornare pharetra quis at eros. Vestibulum finibus justo eget urna aliquet lobortis. Suspendisse efficitur massa id pellentesque rhoncus. Pellentesque lacus ex, vestibulum quis velit ac, rhoncus semper odio. Etiam quis tincidunt risus, non aliquet magna. Maecenas hendrerit, felis non sollicitudin tincidunt, nibh nisi ullamcorper justo, malesuada sollicitudin urna nunc sit amet risus. Donec ac fringilla nibh. Donec vehicula id erat eu suscipit. In et turpis convallis, accumsan dolor vitae, placerat nisl. "
	"Etiam scelerisque odio eget nunc iaculis euismod. Quisque sed nisl placerat, pulvinar quam nec, consectetur dui. Phasellus eu ligula non ipsum mollis dapibus semper non purus. Duis non eros at lectus ultricies packet_messageor. Etiam sit amet nibh lacus. Sed bibendum tortor vitae tortor sollicitudin vestibulum. Cras tristique, risus eu packet_messageor mattis, felis ligula varius mi, eu mattis augue mi sit amet est. Fusce quis ipsum condimentum leo porttitor dictum non et turpis. Nunc packet_messageor at turpis sed consectetur. Pellentesque faucibus dui id ante congue, vel aliquet justo maximus. Nulla at pretium est.")
messtosend = parse_order(message, 500)
print(messtosend)
