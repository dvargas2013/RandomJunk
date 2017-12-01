#!/usr/bin/env python2.6
# pyautogui can do these things

import Quartz.CoreGraphics as CG

def mouseEventLeft(kind, posx, posy):
    CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
            None,kind,(posx,800-posy),CG.kCGMouseButtonLeft))
def mouseEventRight(kind,posx,posy):
    CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(
            None,kind,(posx,800-posy),CG.kCGMouseButtonRight))

def mousemove(posx,posy):
    mouseEventLeft(CG.kCGEventMouseMoved, posx,800-posy)

def mouseclick(posx,posy):
    mouseEventLeft(CG.kCGEventLeftMouseDown, posx,800-posy)
    mouseEventLeft(CG.kCGEventLeftMouseUp, posx,800-posy)
def mouseclickright(posx,posy):
    mouseEventRight(CG.kCGEventRightMouseDown, posx,800-posy)
    mouseEventRight(CG.kCGEventRightMouseUp, posx,800-posy)

def mousedrag(posx,posy, time=0):
    if time<0: mouseEventLeft(CG.kCGEventLeftMouseDown, posx,800-posy)
    mouseEventLeft(CG.kCGEventLeftMouseDragged, posx,800-posy)
    if time>0: mouseEventLeft(CG.kCGEventLeftMouseUp, posx,800-posy)

def scroll(x,y):
    CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateScrollWheelEvent(None, CG.kCGScrollEventUnitLine, 2, y, x))