from socket import socket, AF_INET, SOCK_DGRAM,getaddrinfo,SOL_SOCKET, SO_BROADCAST
from multiprocessing import Queue, Process
from threading import Thread
import time

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
        print(str(data).replace("b'",'').replace("'",''))


# This function broadcasts a message for other other machines running the script on the same local network to add the host ip to their send list
def ping(r,username):
    hostip=get_ip()
    name=username.get()
    broadcastdata=name+':'+str(hostip)
    broadcastdata=broadcastdata.encode('utf-8')
    broadcastsocket=socket(AF_INET, SOCK_DGRAM)
    broadcastsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    hostlist=hostip.split('.')
    while r.running:
        for x in range(256):
            hostlist[3]=str(x)
            broadcastsocket.sendto(broadcastdata,('.'.join(hostlist),5023))
        time.sleep(.5)


# This function listens for the message sent by other machines via the ping function and adds the other machines ips to the send list
def getping(iplist,r,usernamelist,rf):
    hostip=get_ip()
    locatesoc=socket(AF_INET, SOCK_DGRAM )
    locatesoc.bind((hostip,5023))
    while r.running:
        data,addr=locatesoc.recvfrom(1024)
        try:
            data=str(data).replace("b'",'').replace("'",'')
            sentip=data.split(':')[1]
            name=data.split(':')[0]
            if sentip!=hostip:
                    if not sentip in rf.sendaddresslist:
                        rf.sendaddresslist.append(sentip)
                        rf.namelist.append(name)
                        print(name,' Has joined the chat!')
                        iplist.put(rf.sendaddresslist)
                        usernamelist.put(rf.namelist)
        except:
            pass


#this class allows for the closing of all threads
class run():
    def __init__(self):
        self.running=True
        
    def stop(self):
        self.running=False
    
#this class allows for refreshing the ip list
class refresh():
    def __init__(self):
        self.namelist=[]
        self.sendaddresslist=[]
    def Refresh(self):
        self.namelist=[]
        self.sendaddresslist=[]
if __name__ == "__main__":
    #get host ip
    hostip=get_ip()

    # create a Queue to store the list of ip adresses
    iplist=Queue()

    #create queue for username to be sent to ping process
    username=Queue()

    #create queue for storing other machines usernames
    usernamelist=Queue()

    #initiate classes
    r=run()
    rf=refresh()

    #create threads
    serverprocess=Thread(target=serve,args=(r,))
    pingprocess=Thread(target=ping,args=(r,username))
    getpingprocess=Thread(target=getping,args=(iplist,r,usernamelist,rf))

    
    sendsocket=socket(AF_INET, SOCK_DGRAM)

    # user instructions
    print('use: "-quit" to exit the chatroom')
    print('use: "-d" to direct message someone')
    name=input('Enter your name: ')

    #send the username to the ping function 
    username.put(name)


    #start thread to listen for and print messages from other local machines and thread to listen for pings
    serverprocess.start()
    getpingprocess.start()

    #start ping thread
    pingprocess.start()

    ipsendlist=[]
    usernamesendlist=[]
    while True:
        text=input()
        direct=False

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
            break
        #code for direct message
        elif text=='-d':
            print('List of users online:')
            rf.Refresh()
            time.sleep(1)
            while not usernamelist.empty():
                usernamesendlist=usernamelist.get()
            if '' in usernamesendlist:
                sendto=input('enter the name of who you want to send the message to: ')
                
                while not sendto in usernamesendlist:
                    sendto=input('please enter a valid name: ')
                text=input('enter your message: ')
                direct=True
        #creates the final string to send to the list of ip's
        if direct:
            text='[Direct Message] '+name+': '+text
        else:
            text=name+': '+text               #'['+str(hostip)+'] '+name+': '+text

        #Checks for an updated list ip adresses
        while not usernamelist.empty():
            usernamesendlist=usernamelist.get()
        if not iplist.empty():
            while not iplist.empty():
                ipsendlist=iplist.get()
            send=True
        elif ipsendlist==[] :
            send=False
            print('there is no one else in the chatroom yet')
        #sends message to all ip adresses on the list
        if send:
            if direct:
                address= ipsendlist[usernamesendlist.index(sendto)]
                sendsocket.sendto(text.encode('utf-8'),(address,5024))
            else:
                for address in ipsendlist:
                        sendsocket.sendto(text.encode('utf-8'),(address,5024))
        
