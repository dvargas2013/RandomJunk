#!/usr/bin/env python3

from xmlrpc.server import SimpleXMLRPCServer
import struct

server = SimpleXMLRPCServer(("localhost", 0))

with open("/tmp/xmlrpc.prt", "wb") as f:
    f.write(struct.pack(">I",server.server_address[1]))
print(server.server_address[1])

string = [""]
def getData():
    print(string[0])
    return string[0]
def setData(s):
    string[0] = s
    return s
server.register_function(getData, "getData")
server.register_function(setData, "setData")
server.serve_forever()