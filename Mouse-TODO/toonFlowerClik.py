#!/usr/bin/python2.6
from MaskWrapper import MaskWrapper,masks
from __init__ import *
from time import sleep

'''
7 bean flower: pggggyg

triple click on the empty slot

and i will do the rest c;
'''
loop = [(-70,-73),(-124,0),(0,0),(0,0),(0,0),(155,0),(-155,0),(182,134)]
def run(e):
    global loop
    if e.clickCount()==3:
        x,y = e.locationInWindow()
        y = 800-y # window location and mouse clicker start on opposite corners
        
        for i,j in loop:
            sleep(.2)
            x+=i
            y+=j
            mousemove(x,y)
            mouseclick(x,y)

sc = MaskWrapper(masks["LMouse"]["Down"],run)
sc.mainloop()
