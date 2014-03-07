#!/usr/bin/env python
# encoding: utf-8
import send_packet
from player_manager import playerManager
import gwdata
#from team import team
import team
from team_manager import teamManager

#from gwdata import

class Player:

    def __init__(self):
        self.name=""
        #self.team=""
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
        playerManager.add(self)
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
        global playerManager,teamManager
        newTeam = team.Team()
        newTeam.create(self)
        #team.create(self)
        #print '我是队长名:', team.caption
        self.iscaption=1
        self.team=newTeam  # 是指向队伍实例吧.? S 那边只能 self.team=newTeam.name
        teamManager.add(newTeam)
        print "player_73行:新建队伍成员",newTeam.member
        gwdata.drawTeamMember(self)
        playerManager.add(self)
        print "player_75行:已经加入玩家管理,player.iscaption,",self.iscaption
        print "玩家.team.member:",
        print self.team.member
        print '玩家.name',self.name
        regetPlayer = playerManager.get(self.name)
        print "重新获取玩家的队伍实例的 成员"
        print regetPlayer.team.member


    def c2gsInvited(self,invitee):
        packet = send_packet.SendPacket(8)
        #packet.packString(self.name)
        packet.packString(invitee.name)
        packet.send()
        print "发送邀请请求"
    def inviteAskShow(self,inviterName):
        gwdata.inviteAskShow(self,inviterName)
    def c2gsInviteReply(self,answer,inviterName):
        packet = send_packet.SendPacket(9)
        packet.packString(answer)
        packet.packString(inviterName)
        packet.send()
    def inviteAnswerReply(self,answer,inviteeName):
        gwdata.inviteAnswerReply(answer,inviteeName)



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
    iscaption = packet.unpackInt()
    teamName=packet.unpackString()

    newPlayer = Player()
    newPlayer.create(name)
    newPlayer.enterWorld(x,y)
    newPlayer.iscaption=iscaption
    newPlayer.team=teamName
    playerManager.add(newPlayer)

def gs2cOtherExitGame(player,packet):
    name = packet.unpackString()
    playerToExit =playerManager.remotePlayers[name]
    playerToExit.exitGame()
def gs2cTeamCreate(player,packet):
    #playerName=packet.unpackString()
    #playerGeted=playerManager.get(playerName)
    #playerGeted.teamCreate()
    player.teamCreate()
def gs2cOtherTeamCreate(player,packet):
    playerName = packet.unpackString()
    playerGeted = playerManager.get(playerName)
    newTeam = team.Team()
    newTeam.create(playerGeted)
    playerGeted.iscaption =1
    playerGeted.team=newTeam.name
    teamManager.add(newTeam)
    playerManager.add(playerGeted)
def gs2cInviteAsk(player,packet):
    inviterName = packet.unpackString()
    player.inviteAskShow(inviterName)
    #player.inviteAskReply(inviterName)

def gs2cInviteReply(player,packet):
    answer = packet.unpackString()
    inviteeName = packet.unpackString()
    player.inviteAnswerReply(answer,inviteeName)

