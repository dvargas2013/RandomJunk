#!/usr/bin/python2.6
from MaskWrapper import MaskWrapper,masks, NSLeftMouseDown, NSKeyDown
from __init__ import *
from time import sleep

s = 0
def run(e):
    if e.type() == NSKeyDown:
        global s
        print not e.isARepeat(), s
        if not e.isARepeat() and s:
            x,y = e.locationInWindow()
            y = 800-y # window location and mouse clicker start on opposite corners
            for i in range(10):
                for j in range(3):
                    sleep(.2)
                    tx=x+100*i
                    ty=y+120*j
                    mousemove(tx,ty)
                    mouseclick(tx,ty)
        s = e.isARepeat()

sc = MaskWrapper(masks["Board"]["Down"],run)
sc.mainloop()