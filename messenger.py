import socket
from threading import Thread
from Queue import Queue

q = Queue()                                           #create queue to communicate between threads
                                                      #server code
def server():
    q.get()                                                     #prevents printing and taking input from overlapping (reads 'take input la' from client thread)
    ip = raw_input("Enter your IP: ")                           #server enters ip and port - must happen before client does the same
    pnum = int(raw_input("Enter chosen port: "))
    myServ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create new sock of type SOCK_STREAM(TCP) to accept connection
    myServ.bind((ip, pnum))                                     #binds socket to given server ip and host
    myServ.listen(1)                                            #listens for one connection request
    myClient, address = myServ.accept()                         #returns new socket capable of sending and receiving messages
    q.put('client connected')                                   #OKAY for client thread to start
    print("\nConnected to " + (ip) + " on port " + str(pnum))

    while True:                                                 #server only receives
        recv_msg = myClient.recv(2048)                          #server receives message
        if recv_msg == "exit":
            print('\n***Your friend has exited - type \'exit\' to end***\n')
            break
        print("-- "+(recv_msg))
    myClient.close()

def client():
    ip = raw_input("Enter your friend's IP: ")                     #must happen after server has entered socket address
    pnum = int(raw_input("Enter chosen port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #create new sock of type SOCK_STREAM(TCP)
    sock.connect((ip, pnum))                                       #connects to socket at given address
    print("Connected to " + (ip) + " on port " + str(pnum))
    q.put('take input la')                                          #allows server to run

    while True:
        reply = raw_input()                                         #client only sends messages
        sock.sendall(reply)
        if reply == "exit":
             break
    sock.close()

cType = ' '
while cType != 'C' and cType != 'W' and cType != "exit":        #while loop to take input
   cType = raw_input("Exit (exit)\n(C)onnect\n(W)ait for connection\n")


if cType=='W':
    q.put('LOL')                    #dummy q.put so server runs - this q.get is important is user chooses (C)onnect
    server = Thread(target=server)  #sets 'server' to server function
    server.start()                  #starts server thread for receiving
    q.get()                         #prevents client from being started too early and printing while user is inputting - from 'client connected'
    c = Thread(target=client)       #creates client thread for sending
    c.start()
    c.join()
    server.join()


elif cType =='C':
    c = Thread(target=client)        #creates client thread for sending
    c.start()
    s = Thread(target=server)       #starts server thread for receiving
    s.start()
    c.join()
    s.join()
