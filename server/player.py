#!/usr/bin/env python
# encoding: utf-8
from packet import SendPacket

class Player:
    def __init__(self,socket):
        self.socket=socket

    def creat(self,name):
        self.name=name
        self.x=0
        self.y=0
    def enterWorld(self):
        self.gs2cEnterWorld()
    def gs2cEnterWorld(self):
        packet=SendPacket(1)
        packet.packInt(self.x)
        packet.packInt(self.y)
        packet.send(self)

    def move(self,newX,newY):
        self.x=newX
        self.y=newY
        self.gs2cPlayerMove()
    def gs2cPlayerMove(self):
        packet=SendPacket(2)
        packet.packInt(self.x)
        packet.packInt(self.y)
        packet.send(self)

def c2gsEnterWorld(player,packet):
    name = packet.unpackString()
    player.creat(name)
    player.enterWorld()
def c2gsPlayerMove(player,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    player.move(x,y)

