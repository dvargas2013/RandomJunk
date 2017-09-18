#!/usr/bin/python2.6
from Tkinter import *
from __init__ import *
from time import sleep
'''
Move Selected up and down
Duplicate Selected to bottom / Copy paste?
'''
    
class RadioList(Frame):
    def __init__(self, master, List):
        Frame.__init__(self, master)
        self.radios = []
        
        v = StringVar()
        for name in List: self.radios.append(
            Radiobutton(self, text=name, variable=v, value=name).pack(anchor=W)
        )
        self.val = v
        self.val.set('click')
        
class ScrollableList(Frame):
    def __init__(self, master, clickList):
        Frame.__init__(self, master)
        self.l = Listbox(self, selectmode=EXTENDED, width=40)
        self.l.grid(rowspan=6,sticky=N+S)
        
        self.cleanD = Button(self, text="DRAG CLEAN", command=lambda:self.clean('drag'))
        self.cleanD.grid(row=2,column=2,sticky=W+E)
        self.delete = Button(self, text="DELETE", command=self.deleteSelected)
        self.delete.grid(row=2,column=3,sticky=W+E)
        self.cleanM = Button(self, text="MOVE CLEAN", command=lambda:self.clean('move'))
        self.cleanM.grid(row=3,column=2,sticky=W+E)
        self.flip = Button(self, text="FLIP", command=self.flipSelected)
        self.flip.grid(row=3,column=3,sticky=W+E)
        
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.cleanM = Button(self, text="CREATE", command=self.click)
        self.cleanM.grid(row=4,column=2, sticky=S)
        self.edit = Button(self, text="EDIT", command=self.edit)
        self.edit.grid(row=4,column=3, sticky=S+W+E)
        self.kinds = RadioList(self, App.EXEC.keys())
        self.kinds.grid(row=5,column=2,columnspan=2, sticky=N)
        
        self.clickList = clickList
        self.refresh()
        
    def find(self, ind, cond, default=-1):
        for i in range(ind, len(self.clickList)):
            if cond(self.clickList[i][0]): return i
        return default
    def clean(self, name):
        a = -1
        while a:
            a = self.find(a+1,lambda x: x==name, False)
            if a:
                b = self.find(a,lambda x: x!=name, len(self.clickList))
                for i in range(b-2,a,-1): self.clickList.pop(i)
                a+=1
        self.refresh()
    def edit(self):
        for i in reversed(self.l.curselection()):
            self.clickList[int(i)+1][0] = self.kinds.val.get()
        self.refresh()
    def click(self):
        if len(self.clickList)<2: self.clickList[:] = [['start',0,0,0]]
        x,y = self.master.hiddenLastClick[0]
        self.clickList.append([self.kinds.val.get(), x,y, .03125])
        self.refresh()
    def flipSelected(self):
        popit = [int(i)+1 for i in self.l.curselection()]
        while len(popit)>1:
            a,b = popit.pop(0), popit.pop(-1)
            self.clickList[a],self.clickList[b] = self.clickList[b],self.clickList[a]
        self.refresh()
    def deleteSelected(self, *d):
        if len(self.l.curselection())>0:
            save = int(self.l.curselection()[0])
            if save >= self.l.size(): save-=1
            for i in reversed(self.l.curselection()): self.clickList.pop(int(i)+1)
            self.refresh()
            self.l.activate(save)
            self.l.select_set(save)
            self.l.see(save)
    def refresh(self):
        self.l.delete(0,END)
        for i in self.clickList[1:]: self.l.insert(END,i)

class NumberEntry(Entry):
    def __init__(self, master, value="", maxlength=None):
        Entry.__init__(self, master)
        self.maxlength = maxlength
        self.num = value
        self.contentVar = StringVar()
        self.contentVar.set(self.num)
        self.contentVar.trace("w", self.__callback)
        self.config(textvariable=self.contentVar)

    def __callback(self, *trace):
        cur = self.contentVar.get()
        if not cur: cur = '1'
        if self.validate(cur): self.num = cur
        self.contentVar.set(self.num)
        
    def validate(self, value):
        if not self.maxlength or len(value) <= self.maxlength:
            try: return float(value)>=1
            except ValueError: return False
        return False
    
class Instruct(Frame):
    INSTR = '''Welcome to Mouse Copy App.
The window should be on top by now. 
If not click on it. That should focus it.

This program can record mouse clicks, movements and drags.

Pressing 'o' changes screen opacity.
Pressing 'Space' changes the size of the screen. 
(Huge and Tiny to the top-left)
'r' is to start recording (and stop recording).
'Enter' is to play recording starting from selected ;)
'Esc' to close. Any other closing way is good too.'''
    def __init__(self, master):
        Frame.__init__(self,master)
        self.text = Label(self, text=Instruct.INSTR)
        self.text.pack()

        cB = IntVar()
        self.clickBox =  Checkbutton(self, text="Track Clicks", variable=cB)
        self.clickBox.var = cB
        self.clickBox.pack()
        self.clickBox.var.set(1)

        dB = IntVar()
        self.dragBox = Checkbutton(self, text="Track Drags", variable=dB)
        self.dragBox.var = dB
        self.dragBox.pack()
        self.dragBox.var.set(0)
        
        mB = IntVar()
        self.moveBox = Checkbutton(self, text="Track Moves", variable=mB)
        self.moveBox.var = mB
        self.moveBox.pack()
        self.moveBox.var.set(0)
        
        self.speedLabel = Label(self, text="Edit to set Variable Speed")
        self.speedLabel.pack()
        self.speed = NumberEntry(self, maxlength=10, value="3.0")
        self.speed.pack()
        

class App(Tk):
    SMALL = '75x15+0+0'
    BIG = "{0}x{1}+0+0"
    LO = 0.5
    HI = 1.0
    EXEC = {
        'move':mousemove, 
        'click':mouseclick, 
        'drag':mousedrag, 
        'dragfirst': (lambda x,y: mousedrag(x,y,time=-1)), 
        'draglast':(lambda x,y: mousedrag(x,y,time=1))
    }
    
    def __init__(self):
        Tk.__init__(self)
        self.wm_title("Mouse Copy App")
        self.geometry("900x350+0+0")
        self.bind("<Escape>", lambda e: self.destroy())
        
        #Vars
        self.clicks = []
        self.hiddenLastClick = [[-1,-1],[0,0]]
        self.isRecording = False

        #EditList
        self.scrollist = ScrollableList(self, self.clicks)
        self.scrollist.pack(side='left', fill='both', expand=1)
        self.instruct = Instruct(self)
        self.instruct.pack(anchor=N+E)
        
        self.lastClickStr = StringVar()
        self.lastClick = Label(self, textvariable=self.lastClickStr)
        self.lastClickStr.set('[0,0]')
        self.lastClick.pack(side="right")
        
        #Tracking Bindings
        self.bind("<Button-1>", self.leftclick)
        self.bind('<B1-Motion>', self.drag)
        self.bind('<Motion>', self.move)
        
        #Toggle Bindings
        self.bind("r",  self.recordToggle)
        self.bind("o", self.opacityToggle)
        self.bind("<Return>", self.play)
        self.bind("<space>", self.sizeToggle)
        self.bind("<BackSpace>", self.scrollist.deleteSelected)
        
        #Wait till it shows up and make transparent
        Tk.wait_visibility(self)
        self.attributes('-alpha', App.HI)

        #Lift to top and start
        self.lift()
        self.attributes('-topmost', True)
        self.mainloop()
        
    def leftclick(self,event):
        self.hiddenLastClick.append([event.x_root, event.y_root])
        self.hiddenLastClick.pop(0)
        self.lastClickStr.set(self.hiddenLastClick[1])
        if self.isRecording and self.instruct.clickBox.var.get():
            if self.clicks[-1][0]=='drag': self.clicks[-1][0]='draglast'
            self.record(event, 'click')
    def drag(self,event): 
        if self.isRecording and self.instruct.dragBox.var.get():
            if self.clicks[-1][0]=='click': self.clicks[-1][0]='dragfirst'
            self.record(event, 'drag')
    def move(self,event): 
        if self.isRecording and self.instruct.moveBox.var.get():
            if self.clicks[-1][0]=='drag': self.clicks[-1][0]='draglast'
            self.record(event, 'move')
    def record(self, event, kind):        
        self.clicks.append([kind, event.x_root, event.y_root, event.time/1e3])
        #Make Times Relative
        self.clicks[-2][-1] = self.clicks[-1][-1]-self.clicks[-2][-1]
        self.scrollist.refresh()
    def recordToggle(self,event):
        self.isRecording = not self.isRecording
        if len(self.clicks)<2: self.clicks[:] = [['start',0,0,event.time/1e3]]
        else: self.clicks[-1][-1] = event.time/1e3
        if self.isRecording: self.configure(bg='blue')
        else:
            if self.clicks[-1][0]=='drag': self.clicks[-1][0]='draglast'
            self.clicks[-1][-1] = 0
            self.configure(bg='white')
        self.scrollist.refresh()
    def opacityToggle(self, event):
        if self.attributes('-alpha') == App.LO:
            self.attributes('-alpha',App.HI)
        else: self.attributes('-alpha',App.LO)
    def sizeToggle(self, event):
        if (self.winfo_height()>100): self.geometry(App.SMALL)
        else: self.geometry(App.BIG.format(*self.maxsize()))
    def play(self, event):
        if self.isRecording: self.recordToggle(event) 
        self.geometry(App.SMALL)
        self.after(20, self.clickAll)
    def clickAll(self):
        mult = float(self.instruct.speed.num)
        for k,x,y,t in self.clicks:
            k = App.EXEC.get(k,False)
            if k: 
                k(x,y) #TODO Sleep using after 
                sleep(t/mult) #TODO but you need to change when time gets called (pre instead of post)
                #So you need to change how things are recorded
        self.geometry(App.BIG.format(*self.maxsize()))

if __name__ == '__main__': app = App()