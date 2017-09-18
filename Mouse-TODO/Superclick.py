#!/usr/bin/python2.6
from MaskWrapper import MaskWrapper,masks
from __init__ import *

def run(e):
    if e.clickCount()==2:
        x,y = e.locationInWindow()
        for i in xrange(1001): mouseclick(x,800-y)
sc = MaskWrapper(masks["LMouse"]["Down"],run)
sc.mainloop()
