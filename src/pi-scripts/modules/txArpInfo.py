from threading import Thread
from modules.gatewayIP import gatewayIP
from modules.listen_router import listen_router

def txArpInfo():

    # Find the gateway IP 
    # 
    gateway = gatewayIP()
    # Start a thread to continuously run the listen router script
    #
    TXarp = Thread(target=listen_router, args=(gateway))
    TXarp.daemon = True
    TXarp.start()
    return 1
