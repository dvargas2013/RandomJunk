#!/usr/bin/python2.6
from MaskWrapper import MaskWrapper,masks,NSLeftMouseDown,NSRightMouseDown
from __init__ import mouseclick,mouseclickright

clicked = 0
from time import sleep
def run(e):
    global clicked
    if clicked: clicked = 0
    else:
        x,y = e.locationInWindow()
        sleep(.1)
        if   e.type() == NSRightMouseDown: mouseclick(x,y)
        elif e.type() == NSLeftMouseDown: mouseclickright(x,y)
        clicked = 1
sc = MaskWrapper(masks["LMouse"]["Down"] + masks["RMouse"]["Down"],run)
sc.mainloop()