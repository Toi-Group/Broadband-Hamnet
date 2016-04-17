RECEIVERPORT=6006

printmsg="Listing on port: $RECEIVERPORT"
echo $printmsg

nc -vvlnp $RECEIVERPORT >/dev/null
