from threading import Thread
from listen_router import listen_router

def txArpInfo():

    # Start a thread to continuously run the listen router script
    #
    TXarp = Thread(target=listen_router)
    TXarp.daemon = True
    TXarp.start()
    return 1
