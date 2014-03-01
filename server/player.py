#!/usr/bin/env python
# encoding: utf-8
from packet import SendPacket
from player_manager import playerManager
from team import team
from team_manager import teamManager
class Player:
    def __init__(self,socket):
        self.socket    = socket
        self.sendData  = ''
        self.broadBuff = ''
        self.exitKey = 0
        self.team=""
    def creat(self,name):
        self.name=name
        self.x=0
        self.y=0
    def enterWorld(self):
        self.gs2cEnterWorld()
        self.gs2cExistingPlayers()
        self.gs2cOhterEnterWorld()
    def gs2cEnterWorld(self):
        packet=SendPacket(1)
        packet.packInt(self.x)
        packet.packInt(self.y)
        packet.packString(self.name)
        packet.send(self)

    def move(self,newX,newY):
        self.x=newX
        self.y=newY
        self.gs2cPlayerMove()
        self.gs2cOtherMove()
    def gs2cPlayerMove(self):
        packet=SendPacket(2)
        packet.packInt(self.x)
        packet.packInt(self.y)
        packet.packString(self.name)
        packet.send(self)
    def gs2cOhterEnterWorld(self):
        for _,playerOther in playerManager.socketPlayer.items():
            packet=SendPacket(3)
            packet.packInt(self.x)
            packet.packInt(self.y)
            packet.packString(self.name)
            packet.send(playerOther)
    def gs2cOtherMove(self):
        for _,playerOther in playerManager.socketPlayer.items():
            packet=SendPacket(4)
            packet.packInt(self.x)
            packet.packInt(self.y)
            packet.packString(self.name)
            packet.send(playerOther)

    def gs2cExistingPlayers(self):
        """S将其他玩家的x，y ，name 发给 刚刚加入的 player"""
        for _,playerOther in playerManager.socketPlayer.items():
            packet=SendPacket(5)
            packet.packInt(playerOther.x)
            packet.packInt(playerOther.y)
            packet.packString(playerOther.name)
            packet.send(self)
    def gs2cOtherExitGame(self):
        self.exitKey=1
        for _,playerOther in playerManager.socketPlayer.items():
            packet=SendPacket(0)
            packet.packString(self.name)
            packet.send(playerOther)
    def gs2cTeamCreate(self):
        team.create(self)
        teamManager.add(team)
        packet=SendPacket(6)
        packet.packString(self.name)
        packet.send(self)

def c2gsEnterWorld(player,packet):
    name = packet.unpackString()
    player.creat(name)
    player.enterWorld()
def c2gsPlayerMove(player,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    player.move(x,y)

def c2gsExitGame(player,packet):
    player.gs2cOtherExitGame()
def c2gsTeamCreate(player,packet):
    #name = packet.unpackString()
    player.gs2cTeamCreate()


