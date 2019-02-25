import keyboard
from tkinter import*
from time import sleep
def Type(Key):
    global entrylist
    index=0
    keyboard.send('backspace')
    sleep(.01)
    for entry in entrylist:
        if index!=0:
            string=entry.get()
            stringlist=list(string)
            if len(stringlist)>3:
                for x in range(len(stringlist)-3):
                    if stringlist[x]=='!' and stringlist[x+1]=='t' and stringlist[x+2]=='a' and stringlist[x+3]=='b':
                        del stringlist[x+3]
                        del stringlist[x+2]
                        del stringlist[x+1]
                        stringlist[x]='tab'
            if len(stringlist)>5:
                for x in range(len(stringlist)-5):
                    if stringlist[x]=='!' and stringlist[x+1]=='e' and stringlist[x+2]=='n' and stringlist[x+3]=='t' and stringlist[x+4]=='e' and stringlist[x+5]=='r':
                        del stringlist[x+5]
                        del stringlist[x+4]
                        del stringlist[x+3]
                        del stringlist[x+2]
                        del stringlist[x+1]
                        stringlist[x]='enter'
            for key in stringlist:
                keyboard.send(key)
        index+=1
class window():
    def __init__(self):
        global entrylist
        self.root=Tk()
        self.root.config(bg='black')
        screen_width = self.root.winfo_screenwidth()/2
        screen_height = self.root.winfo_screenheight()/6
        ww = screen_width
        h = screen_height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (ww/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (ww, h, x, y))
        self.isfirst=True
        self.vcmd = (self.root.register(self.callback))

        hotkeylabel=Label(self.root,text='Hotkey:',font='bold 20',bg='black',fg='green')
        hotkeylabel.place(x=0,y=0)
        textlabel=Label(self.root,text='Text: (use "!tab" and "!enter" to press tab and enter)',font='bold 20',bg='black',fg='green')
        textlabel.place(relx=.15,y=0)
        entrylist=[Entry(self.root,bg='black',font='bold 50',validate='all',validatecommand=(self.vcmd,'%P'),highlightbackground='green',fg='green',insertbackground='green'),\
            Entry(self.root,bg='black',font='bold 50',fg='green',insertbackground='green',highlightbackground='green',selectforeground='darkgreen',selectbackground='grey10')]

        entrylist[0].place(relx=.02,rely=.2,relwidth=.1,relheight=.8)
        entrylist[0].insert('0','`')
        entrylist[1].place(relx=.12,rely=.2,relwidth=.86,relheight=.8)
        self.prevp=''
        if __name__ == "__main__":
            self.root.mainloop()
    def callback(self,P):
        if len(P)<2:
            if P!='':
                if not self.isfirst:
                    keyboard.unhook(self.val)
                    self.prevp=P
                else:
                    self.prevp=P
                    self.isfirst=False
                self.val=keyboard.on_press_key(P,Type)
            return True
        else:
            return False
if __name__ == "__main__":
    win=window()