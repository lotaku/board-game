#!/usr/bin/env python
# encoding: utf-8
"""
玩家模块
"""
from send_packet import SendPacket
from draw_ import draw
from player_manager import playerManager
class Player:
    def __init__(self):
        self.name=""
        self.team=""
        self.teamName=""
        self.iscaption=0
        self.menu=""

    def create(self,name):
        self.name=name
        self.x=1
        self.y=1

    def enterWorld(self,x,y):
        self.x=x
        self.y=y
        draw.drawPlayer(self)
        playerManager.add(self)

    def move(self,x,y):
        print "消除旧位置的 player"
        draw.erasePlayer(self)
        self.x=x
        self.y=y
        print "移动player"
        draw.drawPlayer(self)
        playerManager.add(self)
    def c2gsEnterWorld(self):
        packet=SendPacket(1)
        packet.packString(self.name)
        packet.send()

    def c2gsPlayerMove(self,x,y):
        playerManager.add(self)
        packet=SendPacket(2)
        packet.packInt(x)
        packet.packInt(y)
        packet.packString(self.name)
        packet.send()
    def c2gsExitGame(self):
        packet=SendPacket(0)
        packet.packInt(self.x)
        packet.packInt(self.y)
        packet.packString(self.name)
        packet.send()
    def exitGame(self):
        print "点击移动前： 消除旧位置的 player"
        draw.erasePlayer(self)
        playerManager.remove(self)
    def c2gsTeamCreate(self):
        packet=SendPacket(6)
        packet.packString(self.name)
        packet.send()

    def teamCreate(self):
        global playerManager,teamManager
        newTeam = team.Team()
        newTeam.create(self)
        self.iscaption=1
        self.team=newTeam  # 是指向队伍实例吧.? S 那边只能 self.team=newTeam.name
        self.teamName=newTeam.name

        teamManager.add(newTeam)
        print "player_73行:新建队伍成员",newTeam.member
        print "player_78行:玩家.team.member:",self.team.member
        gwdata.drawTeamMember(self)
        playerManager.add(self)


    def c2gsInvited(self,invitee):
        packet = SendPacket(8)
        packet.packString(invitee.name)
        print "C 队长 发出 邀请 包 ,被邀请者 -->期待 str name:", invitee.name
        packet.send()
        print "发送邀请请求"
    def inviteAskShow(self,inviterName):
        gwdata.inviteAskShow(self,inviterName)
    def c2gsInviteReply(self,answer,inviterName):
        packet = SendPacket(9)
        packet.packString(answer)
        packet.packString(inviterName)
        packet.send()
    def inviteAnswerReply(self):
        gwdata.inviteAnswerReply(self)

    def c2gsKickOut(self,playerUnderMouse):
        memberName = playerUnderMouse.name
        packet = SendPacket(10)
        packet.packString(memberName)
        packet.send()
    def kickOut(self,inviterName,memberToOut):
        if self.name == inviterName:
            member = playerManager.get(memberToOut)
            member.menu.updateMenuOption([])
            print "被踢玩家清空后的菜单类实例:" ,member.menu
            self.team = teamManager.getByTeamName(self)
            print "获得队长team实例:",self.team
            self.team.removeByName(memberToOut)
            teamManager.add(self.team)
            playerManager.add(self)
            playerManager.add(member)
            print "blit新的队伍,在队长客户端里:"
            gwdata.drawTeamMember(self)
        elif self.name == memberToOut:
            self.menu.updateMenuOption([])
            print "被踢玩家清空后的菜单类实例:" ,self.menu
            teamManager.remove(self.team)
            self.team=""
            gwdata.disDrawTeamMember()
            playerManager.add(self)
            print '在被踢出的玩家客户端里,重新blit队伍所在'
    def c2gsTransferCaptain(self,playerUnderMouse):
        packet = SendPacket(11)
        packet.packString(playerUnderMouse.name)
        packet.send()

    def transferCaption(self,oldCaptionName,newCaptionName):
        oldCaption = playerManager.get(oldCaptionName)
        newCaption = playerManager.get(newCaptionName)
        oldCaption.iscaption=0
        newCaption.iscaption=1
        playerManager.add(oldCaption)
        playerManager.add(newCaption)
        gwdata.drawTeamMember(self)
    def c2gsJoinIn(self,playerUnderMouse):
        packet = SendPacket(12)
        packet.packString(playerUnderMouse.name)
        packet.send()
    def joinIn(self,newMemberName):
        self.team = teamManager.getByTeamName(self)
        self.team.add(newMemberName)
        teamManager.add(self.team)
        gwdata.drawTeamMember(self)
    def c2gsQuitTeam(self,playerUnderMouse):
        packet = SendPacket(13)
        packet.send()
        print "发生退伍请求:"


localPlayer=Player()

def gs2cOtherExitGame():
    pass
def gs2cEnterWorld():
    pass
def gs2cPlayerMove():
    pass
def gs2cOtherEnterWorld():
    pass
def gs2cOtherMove():
    pass
def gs2cExistingPlayers():
    pass
def gs2cTeamCreate():
    pass
def gs2cOtherTeamCreate():
    pass
def gs2cInviteAsk():
    pass
def gs2cInviteReply():
    pass
def gs2cKickOut():
    pass
def gs2cTransferCaptain():
    pass
def gs2cJoinIn():
    pass
def gs2cQuitTeam():
    pass

