#!/usr/bin/env python3

from xmlrpc.client import ServerProxy
from time import sleep

import struct
with open("/tmp/xmlrpc.prt", "rb") as f:
    port = struct.unpack(">I",f.read())[0]

past = ""
print(port)
#with ServerProxy("http://localhost:%s/"%port) as proxy:
# for some reason it doesnt have an exit? so i cant use the with construction
proxy = ServerProxy("http://localhost:%s/"%port)
while 1:
    new = proxy.getData()
    if past != new:
        past = new
        print(past)
    sleep(5)

'''
The problem with rpc is that the client has to initiate the transaction
Like a more standard client/server model I'd imagine'''