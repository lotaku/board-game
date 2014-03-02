#!/usr/bin/env python
# encoding: utf-8
import send_packet
from player_manager import playerManager
import gwdata
from team import team
from team_manager import teamManager

#from gwdata import

class Player:

    def __init__(self):
        self.name=""
        self.team=""
        self.iscaption=0

    def create(self,name):
        self.name=name
        self.x=1
        self.y=1

    def enterWorld(self,x,y):
        self.x=x
        self.y=y
        gwdata.drawPlayer(self)
        playerManager.add(self)
    def move(self,x,y):
        print "点击移动前： 消除旧位置的 player"
        gwdata.erasePlayer(self)
        self.x=x
        self.y=y
        print 'move 后 ,人物的 x,y :',self.x,self.y
        playerManager.add(self)
        print "点击移动 player"
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
        packet.packString(self.name)
        packet.send()
        #print 'c发包：请求移动'
    def c2gsExitGame(self):
        packet=send_packet.SendPacket(0)
        packet.packInt(self.x)
        packet.packInt(self.y)
        packet.packString(self.name)
        packet.send()
    def exitGame(self):
        print "点击移动前： 消除旧位置的 player"
        gwdata.erasePlayer(self)
        playerManager.remove(self)
    def c2gsTeamCreate(self):
        packet=send_packet.SendPacket(6)
        packet.packString(self.name)
        packet.send()

    def teamCreate(self):
        team.create(self)
        #print '我是队长名:', team.caption
        self.iscaption=1
        teamManager.add(team)
        print team.member
        gwdata.drawTeamMember()
        playerManager.add(self)

player=Player()

def gs2cEnterWorld(player,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    name = packet.unpackString()
    player.name = name
    print "解压用户名：",name
    player.enterWorld(x,y)
    playerManager.add(player)
    print "c 收到 s 对： 进入世界的回应 ，获得初始位置，x，y",x,y

def gs2cPlayerMove(player,packet):
#====单客户端代码====
    #x=packet.unpackInt()
    #y=packet.unpackInt()
    #player.move(x,y)
    #playerManager.add(player)
    #print "c 收到 s 对： 请求移动的回应 ，获得新位置，x，y",x,y
#====多客户端代码====
    x=packet.unpackInt()
    y=packet.unpackInt()
    name =packet.unpackString()
    player = playerManager.get(name)
    player.move(x,y)
    playerManager.add(player)
    print "c 收到 s 对： 请求移动的回应 ，获得新位置，x，y",x,y

def gs2cOtherEnterWorld(player,packet):
    """
    新用户加入
    """
    x = packet.unpackInt()
    y = packet.unpackInt()
    name =packet.unpackString()
    newPlayer = Player()
    newPlayer.create(name)
    newPlayer.enterWorld(x,y)
    playerManager.add(newPlayer)


def gs2cOtherMove(player,packet):
    """
    其他客户端用户移动
    """
    x = packet.unpackInt()
    y = packet.unpackInt()
    name =packet.unpackString()
    playerOther = playerManager.get(name)
    playerOther.move(x,y)
    playerManager.add(playerOther)

def gs2cExistingPlayers(player,packet):
    """
    刚进入世界，获取其他用户的资料
    """
    x = packet.unpackInt()
    y = packet.unpackInt()
    name =packet.unpackString()
    newPlayer = Player()
    newPlayer.create(name)
    newPlayer.enterWorld(x,y)
    playerManager.add(newPlayer)

def gs2cOtherExitGame(player,packet):
    name = packet.unpackString()
    playerToExit =playerManager.remotePlayers[name]
    playerToExit.exitGame()
def gs2cTeamCreate(player,packet):
    player.teamCreate()
