from threading import Thread
from modules.listen_router import listen_router

def txArpInfo():

    user_pwd = input("Router Password: ")

    with open("user_pwd.txt", "wt") as f:
        f.write(user_pwd)

    # Start a thread to continuously run the listen router script
    #
    TXarp = Thread(target=listen_router)
    TXarp.daemon = True
    TXarp.start()

