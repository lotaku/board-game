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
    def inviteReply(self,answer,inviter):
        self.gs2cInviteReplay(answer,inviter)
    def gs2cInviteReplay(self,answer,inviter):
        packet = SendPacket(9)
        if answer == "Yes":#在这里,让Server做判断,对么? 毕竟要更新服务器的队伍信息.
            print "邀请者队伍实例",
            print inviter.team
            inviterTeam = teamManager.get(inviter)
            inviterTeam.add(self)
            inviter.team = inviterTeam
            print "复制team 给被邀请者"
            self.team = inviterTeam
            self.teamName = inviterTeam.name

            #更新Server信息
            teamManager.add(inviterTeam)
            playerManager.add(inviter)
            self.updatePlayerOnServer(self,inviter)

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
    def updatePlayerOnServer(*players):
        for playerGet in players:
            teamManager.add(playerGet.team)
            playerManager.add(playerGet)


    def kickOut(self,memberName):
        self.gs2cKickOut(memberName)
        print memberName
        member = playerManager.getPlayerByName(memberName)
        self.team = teamManager.get(self)
        print "玩家的队伍成员",self.team.member
        self.team.remove(member)
        print "成功移除会员 member 实例"
        teamManager.add(self.team)
        playerManager.add(self)
        #self.gs2cKickOut()
    def gs2cKickOut(self,memberName):
        packet = SendPacket(10)
        packet.packString(self.name)
        packet.packString(memberName)
        self.team = teamManager.get(self)
        for member in self.team.member:
            packet.send(member)
        print "成功发送给队伍里的所有人"

    def transferCaption(self,newCaptionName):
        print "self,是队长"
        self.gs2cTransferCaption(newCaptionName)
        #todo 在S 端改变队长信息
        self.iscaption=0
        newCaption = playerManager.getPlayerByName(newCaptionName)
        newCaption.iscaption=1
        newCaption.teamName=self.teamName
        playerManager.add(self)
        playerManager.add(newCaption)
    def gs2cTransferCaption(self,newCaptionName):
        packet = SendPacket(11)
        packet.packString(self.name)#旧 队长名
        packet.packString(newCaptionName)#new 队长名
        print "获得队长的 队伍 实例"
        self.team = teamManager.get(self)
        print "发送包给每个队友实例"
        print "所有的队员实例:",self.team.member
        for member in self.team.member:
            packet.send(member)
    def joinIn(self,captionName):
        print "self 是新队友"
        #更新服务器信息
        caption= playerManager.getPlayerByName(captionName)
        caption.team = teamManager.get(caption)
        caption.team.add(self)
        self.team = caption.team
        teamManager.add(caption.team)
        playerManager.add(caption)

        #self.gs2cJoinIn(captionName)
        self.gs2cJoinIn(caption)

    def gs2cJoinIn(self,caption):
        packet = SendPacket(12)
        packet.packString(caption.name)
        packet.packString(self.name)
        self.packetAllTeamMemberName(packet,caption)
        self.sendToTeamMember(packet,caption)

    def quitTeam(self):
        self.team = teamManager.get(self)
        packet = SendPacket(13)
        packet.packString(self.name)
        self.sendToTeamMember(packet,self)
        #更新服务器信息
        self.team=""
        playerManager.add(self)

    def sendToTeamMember(self,packet,player):
        player.team = teamManager.get(player)
        print "发送包给每个队友实例"
        print "所有的队员实例:",player.team.member
        for member in player.team.member:
            packet.send(member)
    #def sendToTeamMember(self,packet,player):
        #self.team = teamManager.get(self)
        #print "发送包给每个队友实例"
        #print "所有的队员实例:",self.team.member
        #for member in self.team.member:
            #packet.send(member)

    def packetAllTeamMemberName(self,packet,player):
        playerTeam = teamManager.get(player)
        memberNum = len(playerTeam.member)
        packet.packInt(memberNum) # 总队友数
        print "所有队员实例:",playerTeam.member
        for member in playerTeam.member:
            packet.packString(member.name)


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
def c2gsKickOut(player,packet):
    memberName = packet.unpackString()
    player.kickOut(memberName)
def c2gsTransferCaption(player,packet):
    newCaptionName = packet.unpackString()
    player.transferCaption(newCaptionName)
def c2gsJoinIn(player,packet):
    print "player 是想加入的队友"
    captionName = packet.unpackString()
    player.joinIn(captionName)
def c2gsQuitTeam(player,packet):
    #memberName = packet.unpackString()
    player.quitTeam()
