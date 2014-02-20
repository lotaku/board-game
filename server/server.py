#!/usr/bin/env python
# encoding: utf-8
#server/server.py
import net
#import socket
#serverSocket = None
class Server:

    def init(self):
        global serverSocket
        net.beginListen()

    def mainLoop(self):
        net.handlePackets()

server=Server()
server.init()
server.mainLoop()

