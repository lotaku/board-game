#!/usr/bin/env python
# encoding: utf-8
"""
玩家模块
"""
from send_packet import SendPacket
from draw_ import draw
from player_manager import playerManager
from team import Team
from team_manager import teamManager
from invitation import invitation as invitationINS
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
        localPlayer = playerManager.getPlayerByName(self.name)
        print "更新前的localPlayer：", localPlayer.x
        playerManager.add(self)
        print "本地本家的队伍实例self.team",self.team
    def c2gsEnterWorld(self):
        packet=SendPacket(1)
        packet.packString(self.name)
        packet.send()

    def c2gsPlayerMove(self,x,y):
        #playerManager.add(self)
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
        newTeam = Team()
        newTeam.create(self)
        self.iscaption=1
        self.team=newTeam  # 是指向队伍实例吧.? S 那边只能 self.team=newTeam.name
        self.teamName=newTeam.name
        draw.drawTeamMember(newTeam)
        print "创建队伍：" ,self.team
        teamManager.add(newTeam)
        playerManager.add(self)



    def c2gsInvited(self,invitee):
        packet = SendPacket(8)
        packet.packString(invitee.name)
        print "C 队长 发出 邀请 包 ,被邀请者 -->期待 str name:", invitee.name
        packet.send()
        print "发送邀请请求"
    def inviteAskShow(self,inviterName):
        invitationINS.inviteAskShow(self,inviterName)
    def c2gsInviteReply(self,answer,inviterName):
        #answer      = dic["answer"]
        #inviterName = dic["inviterName"]
        packet      = SendPacket(9)
        packet.packString(answer)
        packet.packString(inviterName)
        packet.send()
    def inviteAnswerReply(self):
        invitationINS.inviteAnswerReply(self)

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

def gs2cEnterWorld(localPlayer,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    name = packet.unpackString()
    localPlayer.name = name
    print "解压用户名：",name
    localPlayer.enterWorld(x,y)
    playerManager.add(localPlayer)
    print "c 收到 s 对： 进入世界的回应 ，获得初始位置，x，y",x,y

def gs2cPlayerMove(localPlayer,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    #name =packet.unpackString()
    #player = playerManager.get(name)
    localPlayer.move(x,y)
    #playerManager.add(localPlayer)
    print "c 收到 s 对： 请求移动的回应 ，获得新位置，x，y",x,y
    #print "localPlayer.team",localPlayer.team

def gs2cOtherEnterWorld(player,packet):
    """
    新用户加入
    """
    from player import Player
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
    playerOther = playerManager.getPlayerByName(name)
    playerOther.move(x,y)
    playerManager.add(playerOther)

def gs2cExistingPlayers(player,packet):
    """
    刚进入世界，获取其他用户的资料
    """
    from player import Player
    x = packet.unpackInt()
    y = packet.unpackInt()
    name =packet.unpackString()
    iscaption = packet.unpackInt()
    team=packet.unpackString()
    teamName=packet.unpackString()

    newPlayer = Player()
    newPlayer.create(name)
    newPlayer.enterWorld(x,y)
    newPlayer.iscaption=iscaption
    newPlayer.team=team
    newPlayer.teamName=teamName
    playerManager.add(newPlayer)

def gs2cOtherExitGame(player,packet):
    name = packet.unpackString()
    playerGeted=playerManager.getPlayerByName(name)
    from player import localPlayer
    if localPlayer.name == name:
        import pygame,sys
        pygame.QUIT
        sys.exit()
    playerGeted.exitGame()
def gs2cTeamCreate(player,packet):
    player.teamCreate()
def gs2cOtherTeamCreate(player,packet):
    playerName = packet.unpackString()
    teamName= packet.unpackString()
    playerGeted = playerManager.getPlayerByName(playerName)
    newTeam = Team()
    newTeam.create(playerGeted)
    playerGeted.iscaption =1
    playerGeted.team=newTeam.name
    playerGeted.teamName=teamName
    teamManager.add(newTeam)
    playerManager.add(playerGeted)
def gs2cInviteAsk(player,packet):
    inviterName = packet.unpackString()
    player.inviteAskShow(inviterName)

def gs2cInviteReply(player,packet):
    answer      = packet.unpackString() # 答复
    inviterName = packet.unpackString() #邀请者名字
    inviteeName = packet.unpackString()#被邀请者名字
    #发送给队伍所有人
    memberNum = packet.unpackInt() # 总队友数
    members=[]
    for _ in range(memberNum):
        memberName = packet.unpackString()
        member = playerManager.getPlayerByName(memberName)
        members.append(member)
    inviter = playerManager.getPlayerByName(inviterName)
    invitee = playerManager.getPlayerByName(inviteeName)

    invitationINS.inviteAnswerReply(
            answer, members,
            inviter, invitee)

def gs2cKickOut(player,packet):
    inviterName = packet.unpackString()
    memberToOut= packet.unpackString()
    player.kickOut(inviterName,memberToOut)
def gs2cTransferCaptain(player,packet):
    oldCaptionName = packet.unpackString()
    newCaptionName = packet.unpackString()
    player.transferCaption(oldCaptionName,newCaptionName)



def gs2cJoinIn(player,packet):
    captionName= packet.unpackString()
    newMemberName = packet.unpackString()
    memberNum = packet.unpackInt()
    caption = playerManager.get(captionName)
    if player.name == newMemberName:
        newTeam = team.Team()
        newTeam.create(caption)
        memberNumList = range(memberNum)
        for i in memberNumList:
            memberName = packet.unpackString()
            newTeam.add(memberName)
        player.team = newTeam
        playerManager.add(player)
        teamManager.add(player.team)
        gwdata.drawTeamMember(player)
    else:
        player.team = teamManager.getByTeamName(player)
        player.team.add(newMemberName)
        playerManager.add(player)
        teamManager.add(player.team)
        gwdata.drawTeamMember(player)

def gs2cQuitTeam(player,packet):
    memberName = packet.unpackString()
    member =playerManager.getPlayerByName(memberName)
    if player.name == memberName:
        player.team=""
        playerManager.add(player)
        draw.disDrawTeamMember()
    else:
        player.team.remove(member)
        draw.drawTeamMember(player.team)
