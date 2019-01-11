import base64, random, sys, time
from multiprocessing import Process,Queue
#when using this script the argument syntax is: -filename -password -keylength(optional, defaults to 30)

#s is the input string
#n is the number of lists the input string is split into
#m is the group size of the groups of sublists
def mov(s,n,m):
    l=list(s)
    l1=[]
    if n>int(.5*len(l)):
        n=int(.5*len(l))
    rem=len(l)%n
    if len(l)%n==0:
        #this is the mov function code for if the number of charecters in the base64 string
        #fit perfectly in the number of groups
        for y in range(n):
            l11=[]
            for x in range(int(y*(len(l)/n)),int((y*(len(l)/n))+(len(l)/n))):
                l11.append(l[x])
            l1.append(l11)
        y=0
        b1=[]
        #this section takes the list of lists and makes a new list of lists
        #with groups of 2 or 5 in reversed order and the contents of each sublist reversed as well
        
        #groups of 2 section:
        if m==2:
            for sublist in l1:
                y=y+1
                sublist.reverse()
                if y%2==0:
                    num=0
                    
                    b1.append(sublist)
                    b1.append(sl)
                else:
                    num=1
                    sl=sublist
            if num==1:
                   b1.append(sl)
        #groups of 5 section:
        elif m==5:
            for sublist in l1:
               y=y+1
               sublist.reverse()
               if y%5==0:
                   y=0
                   num=0
                   b1.append(sublist)
                   b1.append(s4)
                   b1.append(s3)
                   b1.append(s2)
                   b1.append(s1)
               else:
                   if y%4==0:
                       num=1
                       s4=sublist
                   else:
                       if y%3==0:
                           num=2
                           s3=sublist
                       else:
                           if y%2==0:
                               num=3
                               s2=sublist
                           else:
                               num=4
                               s1=sublist
            if num==1:
                   b1.append(s4)
                   b1.append(s3)
                   b1.append(s2)
                   b1.append(s1)
            elif num==2:
                   b1.append(s3)
                   b1.append(s2)
                   b1.append(s1)
            elif num==3:
                   b1.append(s2)
                   b1.append(s1)
            elif num==4:
                   b1.append(s1)
        #this joins the sublists into strings
        for x in range(n):
            b1[x]=''.join(b1[x])
        #this joins the main list back to one string
        b1=''.join(b1)
    else:
        #this is the mov function code for if the number of charecters in the base64 string
        #doesn't fit perfectly into the number of groups
        for y in range(n):
            l11=[]
            for x in range(int(y*((len(l)-rem)/n)),int((y*((len(l)-rem)/n))+((len(l)-rem)/n))):
                l11.append(l[x])
            l1.append(l11)
        rems=[]
        for x in range(len(l)-rem,len(l)):
            rems.append(l[x])
        y=0
        b1=[]
        #this section takes the list of lists and makes a new list of lists
        #with groups of 2 or 5 in reversed order and the contents of each sublist reversed as well
        #groups of 2 section:
        if m==2:
            for x in l1:
                y=y+1
                if y%2==0:
                    num=0
                    b1.append(x)
                    b1.append(sl)
                else:
                    num=1
                    sl=x
            if num==1:
                   b1.append(sl)
        #groups of 5 section:
        elif m==5:
            for x in l1:
               y=y+1
               if y%5==0:
                   y=0
                   num=0
                   b1.append(x)
                   b1.append(s4)
                   b1.append(s3)
                   b1.append(s2)
                   b1.append(s1)
               else:
                   if y%4==0:
                       num=1
                       s4=x
                   else:
                       if y%3==0:
                           num=2
                           s3=x
                       else:
                           if y%2==0:
                               num=3
                               s2=x
                           else:
                               num=4
                               s1=x
            if num==1:
                   b1.append(s4)
                   b1.append(s3)
                   b1.append(s2)
                   b1.append(s1)
            elif num==2:
                   b1.append(s3)
                   b1.append(s2)
                   b1.append(s1)
            elif num==3:
                   b1.append(s2)
                   b1.append(s1)
            elif num==4:
                   b1.append(s1)
        #this joins the sublists back into strings
        for x in range(n):
            b1[x]=''.join(b1[x])
        #this joins the main list back to one string
        b1=''.join(b1)+''.join(rems)
    #returns the final string
    return b1
#function that actually calls the mov function and is the target of the new processes 
def encryption(string,key,queue,direction):
    x=0
    if direction:
        while x<len(key):
            y=x+1
            if key[x]==0:
                movvar=2
            else:
                movvar=5
            string=mov(string,key[y],movvar)
            x+=2
            print('|',end='',flush=True)
    else:
        while x<len(key):
            y=x+1
            if key[y]==0:
                movvar=2
            else:
                movvar=5
            string=mov(string,key[x],movvar)
            x+=2
            print('|',end='',flush=True)
    queue.put(string)
#function called for encryping a file args are the base64 encoded file and the password
def encrypt(file,pas,keylength):
    direction=False
    #creates the key for encryption using the password to seed the random number generator
    random.seed(pas)
    key=[]
    while keylength%2!=0:
        keylength=int(input('please enter valid keylength'))
    for num in range(keylength):
        key.append(random.randint(2,int(len(file)*.5)))
        key.append(random.randint(0,1))
        key.append(random.randint(2,20))
        key.append(random.randint(0,1))
    if len(file)>100:
        multi=True
    else:
        multi=False
    if multi:
        c1=0
        c2=3
        c3=2
        c4=1
        file1=[]
        file2=[]
        file3=[]
        file4=[]
        
        print('Starting:')
        print('_'*(keylength*2))

        for char in file:
            if c1%4==0:
                file1.append(char)
            elif c2%4==0:
                file2.append(char)
            elif c3%4==0:
                file3.append(char)
            elif c4%4==0:
                file4.append(char)
            c1+=1
            c2+=1
            c3+=1
            c4+=1
        key1=key[0:int(len(key)/4)]
        key2=key[int(len(key)/4):int(len(key)/2)]
        key3=key[int(len(key)/2):int(3*(len(key)/4))]
        key4=key[int(3*(len(key)/4)):len(key)]
    else:
        key1=key
        file1=file
    queue1=Queue()
    p1=Process(target=encryption,args=(file1,key1,queue1,direction))
    p1.start()
    if multi:
        queue2=Queue()
        queue3=Queue()
        queue4=Queue()
        p2=Process(target=encryption,args=(file2,key2,queue2,direction))
        p3=Process(target=encryption,args=(file3,key3,queue3,direction))
        p4=Process(target=encryption,args=(file4,key4,queue4,direction))
        p2.start()
        p3.start()
        p4.start()
    if multi:
        mixed1=queue1.get()
        mixed2=queue2.get()
        mixed3=queue3.get()
        mixed4=queue4.get()
        print('\nFinishing')
        c1=0
        c2=3
        c3=2
        c4=1
        fnumlist=[0,0,0,0]
        final=[]
        for charnum in range(len(file)):
            if c1%4==0:
                final.append(mixed1[fnumlist[0]])
                fnumlist[0]=fnumlist[0]+1
            elif c2%4==0:
                final.append(mixed2[fnumlist[1]])
                fnumlist[1]=fnumlist[1]+1
            elif c3%4==0:
                final.append(mixed3[fnumlist[2]])
                fnumlist[2]=fnumlist[2]+1
            elif c4%4==0:
                final.append(mixed4[fnumlist[3]])
                fnumlist[3]=fnumlist[3]+1
            c1+=1
            c2+=1
            c3+=1
            c4+=1
        final=''.join(final)
    else:
        final=queue1.get()
    return final
#same as above function but for decrypting
def decrypt(file,pas,keylength):
    direction=True
    #creates the key for encryption using the password to seed the random number generator
    random.seed(pas)
    key=[]
    while keylength%2!=0:
        keylength=int(input('please enter valid keylength'))
    for num in range(keylength):
        key.append(random.randint(2,int(len(file)*.5)))
        key.append(random.randint(0,1))
        key.append(random.randint(2,20))
        key.append(random.randint(0,1))
    if len(file)>100:
        multi=True
    else:
        multi=False
    if multi:
        c1=0
        c2=3
        c3=2
        c4=1
        file1=[]
        file2=[]
        file3=[]
        file4=[]
        print('Starting:')
        print('_'*(keylength*2))
        for char in file:
            if c1%4==0:
                file1.append(char)
            elif c2%4==0:
                file2.append(char)
            elif c3%4==0:
                file3.append(char)
            elif c4%4==0:
                file4.append(char)
            c1+=1
            c2+=1
            c3+=1
            c4+=1
        key1=key[0:int(len(key)/4)]
        key2=key[int(len(key)/4):int(len(key)/2)]
        key3=key[int(len(key)/2):int(3*(len(key)/4))]
        key4=key[int(3*(len(key)/4)):len(key)]
        key1.reverse()
        key2.reverse()
        key3.reverse()
        key4.reverse()
    else:
        key1=key
        file1=file
    queue1=Queue()
    p1=Process(target=encryption,args=(file1,key1,queue1,direction))
    p1.start()
    if multi:
        queue2=Queue()
        queue3=Queue()
        queue4=Queue()
        p2=Process(target=encryption,args=(file2,key2,queue2,direction))
        p3=Process(target=encryption,args=(file3,key3,queue3,direction))
        p4=Process(target=encryption,args=(file4,key4,queue4,direction))
        p2.start()
        p3.start()
        p4.start()
    if multi:
        mixed1=queue1.get()
        mixed2=queue2.get()
        mixed3=queue3.get()
        mixed4=queue4.get()
        print('\nFinishing')
        c1=0
        c2=3
        c3=2
        c4=1
        fnumlist=[0,0,0,0]
        final=[]
        for charnum in range(len(file)):
            if c1%4==0:
                final.append(mixed1[fnumlist[0]])
                fnumlist[0]=fnumlist[0]+1
            elif c2%4==0:
                final.append(mixed2[fnumlist[1]])
                fnumlist[1]=fnumlist[1]+1
            elif c3%4==0:
                final.append(mixed3[fnumlist[2]])
                fnumlist[2]=fnumlist[2]+1
            elif c4%4==0:
                final.append(mixed4[fnumlist[3]])
                fnumlist[3]=fnumlist[3]+1
            c1+=1
            c2+=1
            c3+=1
            c4+=1
        final=''.join(final)
    else:
        final=queue1.get()
    return final
# is the user interface portion of the code which takes the arguments,
# reads and writes the files, and encodes/decodes the files to/from 
# base64 strings before and after encryption
if __name__ == "__main__":
        if len(sys.argv)<3:
            print('Please specify file name, password and keylength(optional, default=30) respectively')
        else:
                if len(sys.argv)>3:
                    keylength=int(sys.argv[3])
                else:
                    keylength=30
                path=sys.argv[1]
                password=sys.argv[2]
                if 'zrip' in path:
                        print('Decrypting: ',path)
                        with open(path,'rb') as file:
                            encoded=base64.b64encode(file.read())
                        string=str(encoded).replace("b'",'').replace("'",'').replace('=','')
                        string=decrypt(string,password,keylength)
                        string+='==='
                        string=string.encode()
                        wpath=path.replace('.zrip','')
                        with open(wpath,'wb') as out:
                            out.write(base64.b64decode(string))
                else:
                        print('Encrypting: ',path)
                        with open(path,'rb') as file:
                            encoded=base64.b64encode(file.read())
                        string=str(encoded).replace("b'",'').replace("'",'').replace('=','')
                        string=encrypt(string,password,keylength)
                        string+='==='
                        string=string.encode()
                        with open(path+'.zrip','wb') as out:
                            out.write(base64.b64decode(string))
        print('Done')
