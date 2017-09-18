#!/usr/bin/python2.6
from Cocoa import *
from Foundation import NSObject
from PyObjCTools import AppHelper

masks = {
    "LMouse": { "Down":NSLeftMouseDownMask, "Drag":NSLeftMouseDraggedMask, "Up":NSLeftMouseUpMask },
    "RMouse": { "Down":NSRightMouseDownMask,"Drag":NSRightMouseDraggedMask,"Up":NSRightMouseUpMask},
    "Mouse": { "Move": NSMouseMovedMask, "Wheel": NSScrollWheelMask }, 
    "Board": {"Down": NSKeyDownMask, "Up":NSKeyUpMask } #Require assistive services
}

class MaskWrapper:
    def __init__(self, mask, run):
        self.run = run
        self.mask = mask
    def createAppDelegate (self) :
        sc = self
        class AppDelegate(NSObject):
            def applicationDidFinishLaunching_(self, notification):
                NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(sc.mask, sc.handler)
                print('ready')
        return AppDelegate
    def mainloop(self):
        NSApplication.sharedApplication()
        delegate = self.createAppDelegate().alloc().init()
        NSApp().setDelegate_(delegate)
        self.workspace = NSWorkspace.sharedWorkspace()
        AppHelper.runEventLoop()
    def cancel(self): AppHelper.stopEventLoop()
    def handler(self, event):
        try: self.run(event)
        except ( KeyboardInterrupt ) as e:
            print 'handler', e
            AppHelper.stopEventLoop()

if __name__ == '__main__':
    def run(e): print e
    sc = MaskWrapper(masks["Mouse"]["Wheel"],run)
    sc.mainloop()
