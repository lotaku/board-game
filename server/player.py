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
        self.teamName=""
        self.iscaption=0
        self.name = ''
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
        """S将其他玩家的x，y ，name等信息 发给 刚刚加入的 player"""
        for _,playerOther in playerManager.socketPlayer.items():
            packet=SendPacket(5)
            packet.packInt(playerOther.x)
            packet.packInt(playerOther.y)
            packet.packString(playerOther.name)
            packet.packInt(playerOther.iscaption)
            packet.packString(playerOther.team)
            packet.packString(playerOther.teamName)
            packet.send(self)
    def gs2cOtherExitGame(self):
        self.exitKey=1
        for _,playerOther in playerManager.socketPlayer.items():
            packet=SendPacket(0)
            packet.packString(self.name)
            packet.send(playerOther)
    def teamCreate(self):
        team.create(self)
        self.iscaption=1
        self.team=team.name
        self.teamName=team.name
        teamManager.add(team)
        playerManager.add(self)
        self.gs2cTeamCreate()
        self.gs2cOtherTeamCreate()
    def gs2cTeamCreate(self):
        packet=SendPacket(6)
        packet.packString(self.name)
        packet.send(self)

    def gs2cOtherTeamCreate(self):
        for _,playerOther in playerManager.socketPlayer.items():
            packet=SendPacket(7)
            packet.packString(self.name)
            packet.packString(self.teamName)
            packet.send(playerOther)
    def inviteAsk(self,inviter):
        self.gs2cInviteAsk(inviter)
    def gs2cInviteAsk(self,inviter):
        packet = SendPacket(8)
        packet.packString(inviter.name)
        packet.send(self)
    #def inviteReply(self,answer,inviteeName):
        #self.gs2cInviteReplay(answer,inviteeName)
    def inviteReply(self,answer,inviter):
        self.gs2cInviteReplay(answer,inviter)
    #def gs2cInviteReplay(self,answer,inviteeName):
        #packet = SendPacket(9)
        #packet.packString(answer)
        #packet.packString(inviteeName)
        #packet.send(self)
    def gs2cInviteReplay(self,answer,inviter):
        packet = SendPacket(9)
        if answer == "Yes":#在这里,让Server做判断,对么? 毕竟要更新服务器的队伍信息.
            print "邀请者队伍实例",
            print inviter.team
            inviterTeam = teamManager.get(inviter)
            inviterTeam.add(self)
            #更新Server信息
            teamManager.add(inviterTeam)
            playerManager.add(inviter)

            packet.packString(answer) # 答复
            packet.packString(inviter.name) #邀请者名字
            packet.packString(self.name)#被邀请者名字
            #发送给队伍所有人
            #memberNum = len(inviter.team.member)
            memberNum = len(inviterTeam.member)
            packet.packInt(memberNum) # 总队友数
            for member in inviterTeam.member:
                packet.packString(member.name)
            for member in inviterTeam.member:
                packet.send(member)
        #if answer == "Yes":#在这里,让Server做判断,对么? 毕竟要更新服务器的队伍信息.
            #print "邀请者队伍实例",
            #print inviter.team
            #inviter.team = teamManager.get(inviter.team)
            #inviter.team.add(self)
            ##更新Server信息
            #teamManager.add(inviter.team)
            #playerManager.add(inviter)

            #packet.packString(answer) # 答复
            #packet.packString(inviter.name) #邀请者名字
            #packet.packString(self.name)#被邀请者名字
            ##发送给队伍所有人
            #memberNum = len(inviter.team.member)
            #packet.packInt(memberNum) # 总队友数
            #for member in inviter.team.member:
                #packet.packString(member.name)
            #for member in inviter.team.member:
                #packet.send(member)


def c2gsEnterWorld(player,packet):
    name = packet.unpackString()
    player.creat(name)
    playerManager.add(player)
    player.enterWorld()
def c2gsPlayerMove(player,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    player.move(x,y)

def c2gsExitGame(player,packet):
    player.gs2cOtherExitGame()
def c2gsTeamCreate(player,packet):
    #player.gs2cTeamCreate()
    player.teamCreate()

def c2gsInvited(player,packet):
    inviteeName=packet.unpackString()
    invitee = playerManager.getPlayerByName(inviteeName)
    invitee.inviteAsk(player)
#def c2gsInviteReplay(player,packet):
    #inviteeName=player.name
    #answer = packet.unpackString()
    #inviterName= packet.unpackString()
    #inviter = playerManager.getPlayerByName(inviterName)
    #inviter.inviteReply(answer,inviteeName)

def c2gsInviteReplay(player,packet):
    answer = packet.unpackString()
    inviterName= packet.unpackString()
    inviter = playerManager.getPlayerByName(inviterName)
    #player,这里是指被邀请者
    player.inviteReply(answer,inviter)
