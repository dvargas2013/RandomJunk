#!/usr/bin/env python3

import mmap
from time import sleep

past = ""
with open("/tmp/hello.txt", "r+b") as f:
    with mmap.mmap(f.fileno(), 0) as mm:
        while 1:
            if past != mm[:64]:
                past = mm[:64]
                print(past)
            sleep(1)
pass

'''
The problem with memory map is that
they have to use the memory both as data
and as the control space
dont write unless space is cleared
or a consumer-producer model where it uses appends and pops instead
this '''