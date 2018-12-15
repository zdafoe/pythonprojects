from socket import socket, AF_INET, SOCK_DGRAM,getaddrinfo,SOL_SOCKET, SO_BROADCAST
from multiprocessing import Queue, Process
from threading import Thread
import time
import sys
import os


# This function returns the host ip adress
def get_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


#this function listens for messages sent to the host ip
def serve(r):
    PORT_NUMBER = 5024
    SIZE = 1024
    hostip = get_ip()
    mySocket = socket( AF_INET, SOCK_DGRAM )
    mySocket.bind( (hostip, PORT_NUMBER) )
    while r.running:
        (data,addr) = mySocket.recvfrom(SIZE)
        if str(data).split(':')!='local IM at':
            print(str(data).replace("b'",'').replace("'",''))


# This function broadcasts a message for other other machines running the script on the same local network to add the host ip to their send list
def ping(r):
    hostip=get_ip()
    broadcastdata='local IM at:'+str(hostip)
    broadcastdata=broadcastdata.encode('utf-8')
    broadcastsocket=socket(AF_INET, SOCK_DGRAM)
    broadcastsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    hostlist=hostip.split('.')
    while r.running:
        for x in range(256):
            hostlist[3]=str(x)
            broadcastsocket.sendto(broadcastdata,('.'.join(hostlist),5023))
        time.sleep(2)


# This function listens for the message sent by other machines via the ping function and adds the other machines ips to the send list
def getping(iplist,r):
    hostip=get_ip()
    locatesoc=socket(AF_INET, SOCK_DGRAM )
    locatesoc.bind((hostip,5023))
    sendaddresslist=[]
    while r.running:
        data,addr=locatesoc.recvfrom(1024)
        try:
            data=str(data).replace("b'",'').replace("'",'')
            sentip=data.split(':')[1]
            if sentip!=hostip:
                    if not sentip in sendaddresslist:
                        sendaddresslist.append(sentip)
                        print(sentip,' Has joined the chat!')
                        iplist.put(sendaddresslist)
        except:
            pass


#this class allows for the closing of all threads
class run():
    def __init__(self):
        self.running=True
    def stop(self):
        self.running=False


if __name__ == "__main__":
    hostip=get_ip()
    # create a Queue to store the list of ip adresses
    iplist=Queue()

    r=run()

    #create threads
    serverprocess=Thread(target=serve,args=(r,))
    pingprocess=Thread(target=ping,args=(r,))
    getpingprocess=Thread(target=getping,args=(iplist,r))


    #start ping and ping recieving threads
    pingprocess.start()
    getpingprocess.start()
    sendsocket=socket(AF_INET, SOCK_DGRAM)

    # user instructions
    print('use: "-quit" to exit the chatroom')
    name=input('Enter your name: ')


    #start thread to listen for and print messages from other local machines
    serverprocess.start()
    ipsendlist=[]
    while True:
        text=input()

        # code for stopping all threads
        if text=='-quit':
            r.stop()
            broadcastsocket=socket(AF_INET, SOCK_DGRAM)
            broadcastsocket.sendto(b'',(hostip,5023))
            broadcastsocket.sendto(b'',(hostip,5024))
            iplist.put('')
            serverprocess.join()
            pingprocess.join()
            getpingprocess.join()
            try:
                os.remove("LANCHATIPS.temp")
            except:
                pass
            break
        #creates the final string to send to the list of ip's
        text='['+str(hostip)+'] '+name+': '+text

        #Checks for an updated list ip adresses
        if not iplist.empty():
            while not iplist.empty():
                ipsendlist=iplist.get()
            send=True
        elif ipsendlist==[] :
            send=False
            print('there is no one else in the chatroom yet')
        #sends message to all ip adresses on the list
        if send:
            for address in ipsendlist:
                    sendsocket.sendto(text.encode('utf-8'),(address,5024))
