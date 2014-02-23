#!/usr/bin/env python
# encoding: utf-8
import send_packet
from player_manager import playerManager
import gwdata
#from gwdata import

class Player:

    def __init__(self):
        self.name=""

    def create(self,name):
        self.name=name
        self.x=1
        self.y=1

    def enterWorld(self,x,y):
        self.x=x
        self.y=y
        gwdata.drawPlayer(self)
    def move(self,x,y):
        gwdata.erasePlayer(self)
        self.x=x
        self.y=y
        gwdata.drawPlayer(self)

    def c2gsEnterWorld(self):
        packet=send_packet.SendPacket(1)
        packet.packString(self.name)
        packet.send()
        #print 'c发包：请求进入游戏'

    def c2gsPlayerMove(self,x,y):
        packet=send_packet.SendPacket(2)
        packet.packInt(x)
        packet.packInt(y)
        #packet.packString(self.name)
        packet.send()
        #print 'c发包：请求移动'

player=Player()

def gs2cEnterWorld(player,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    player.enterWorld(x,y)
    playerManager.add(player)
    print "c 收到 s 对： 进入世界的回应 ，获得初始位置，x，y",x,y

def gs2cPlayerMove(player,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    player.move(x,y)
    playerManager.add(player)
    #print "c 收到 s 对： 请求移动的回应 ，获得新位置，x，y",x,y

