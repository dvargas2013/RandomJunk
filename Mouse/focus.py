#!/usr/bin/python
'''
there was an application that needed to be focused every time. 
cause clicks would sometimes go through it.
and hit the finder.
so i posisioned it on the top left
and the computer clicks it and returns the mouse where it was
'''
try:
    from AppKit import NSWorkspace
except ImportError:
    print "Can't import AppKit -- maybe you're running python from brew?"
    print "Try running with Apple's /usr/bin/python instead."
    exit(1)

from datetime import datetime
from time import sleep

from os import system
from __init__ import mouseclick,mousemove
from MousePos import start,mouse,end

def onchange(newname):
    save = mouse(p)
    if newname == "Finder":
        print save
        mouseclick(271,49)
        mousemove(*save)

p=start()
last_active_name = None
try:
    while True:
        active_app = NSWorkspace.sharedWorkspace().activeApplication()
        if active_app['NSApplicationName'] != last_active_name:
            last_active_name = active_app['NSApplicationName']
            print '%s: %s [%s]' % (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                active_app['NSApplicationName'],
                active_app['NSApplicationPath']
            )
        onchange(last_active_name)
        sleep(.1)
except: pass
finally: end()