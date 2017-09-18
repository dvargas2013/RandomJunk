'''
Make circles when Caps Lock is off.
Basically Caps lock is how to stop it.
Must be run from Terminal
'''

from __init__ import mousemove
from math import sin, cos, pi
from time import sleep
import subprocess

from os import path
gk = path.join( path.dirname( path.abspath(__file__) ), 'getKeys')

def Circle(radius=300, center=(600,400)):
    x0,y0 = center
    for t in xrange(0,360,1):
        t = t*pi/180
        mousemove(
            radius*cos(t) + x0,
            radius*sin(t) + y0
        )
        sleep(.002)
def checkCaps():
    "Return True if CapsLock On or recently turned off"
    #return bool(int(subprocess.check_output('/opt/X11/bin/xset q | grep LED',shell=True)[-2]))
    return bool(int(subprocess.check_output(gk)))

def main():
    while 1:
        if checkCaps(): sleep(5)
        else: Circle()

if __name__ == '__main__': main()