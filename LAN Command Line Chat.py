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
                        iplist.put(sendaddresslist)
        except:
            pass
# this process notifies the user if others have joined the groupchat and writes the send list to a temporary file to be used in sending texts in the groupchat
def listupdate(iplist,r):
    l2=[]
    while r.running:
        l1=iplist.get()
        if l2!=l1:
            for x in range(len(l2),len(l1)):
                print(l1[x],' Has joined the chat!')
            l2=l1
            f=open('LANCHATIPS.temp','w')
            f.write(','.join(l1))
            f.close()
        time.sleep(.11)
#this class allows for the closing of all threads
class run():
    def __init__(self):
        self.running=True
    def stop(self):
        self.running=False
if __name__ == "__main__":
    hostip=get_ip()
    iplist=Queue()
    r=run()
    serverprocess=Thread(target=serve,args=(r,))
    pingprocess=Thread(target=ping,args=(r,))
    getpingprocess=Thread(target=getping,args=(iplist,r))
    lsprocess=Thread(target=listupdate,args=(iplist,r))
    serverprocess.start()
    pingprocess.start()
    getpingprocess.start()
    sendsocket=socket(AF_INET, SOCK_DGRAM)
    sendaddresslist=[]
    print('use: "-quit" to exit the chatroom')
    name=input('Enter your name: ')
    gg.start()
    while True:
        text=input()
        if text=='-quit':
            r.stop()
            broadcastsocket=socket(AF_INET, SOCK_DGRAM)
            hostlist=hostip.split('.')
            broadcastsocket.sendto(b'',(hostip,5023))
            broadcastsocket.sendto(b'',(hostip,5024))
            iplist.put('')
            serverprocess.join()
            pingprocess.join()
            getpingprocess.join()
            lsprocess.join()
            try:
                os.remove("LANCHATIPS.temp")
            except:
                pass
            break
        text='['+str(hostip)+'] '+name+': '+text
        try:
            f=open('LANCHATIPS.temp','r')
            fl=f.read()
            fl=fl.split(',')
            if len(fl)>0:
                send=True
            else:
                send=False
        except:
            fl=[]
            send=False
            print('there is no one else in the chatroom yet')
        if send:
            for address in fl:
                    sendsocket.sendto(text.encode('utf-8'),(address,5024))
