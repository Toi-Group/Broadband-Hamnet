RECEIVERIP="10.119.197.28"
RECEIVERPORT=6006


printmsg="Sending data to: ($RECEIVERIP) over Port: ($RECEIVERPORT)"
echo $printmsg

dd if=/dev/zero bs=1K count=100 | nc -vvn $RECEIVERIP $RECEIVERPORT

printmsg="Pinging ($RECEIVERIP)"
echo $printmsg

ping -c 5 $RECEIVERIP