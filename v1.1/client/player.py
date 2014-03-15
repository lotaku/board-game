#!/usr/bin/env python
# encoding: utf-8
import send_packet
from player_manager import playerManager
import gwdata
import team
from team_manager import teamManager
import menu

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

    def c2gsPlayerMove(self,x,y):
        playerManager.add(self)
        packet=send_packet.SendPacket(2)
        packet.packInt(x)
        packet.packInt(y)
        packet.packString(self.name)
        packet.send()
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
        self.iscaption=1
        self.team=newTeam  # 是指向队伍实例吧.? S 那边只能 self.team=newTeam.name
        self.teamName=newTeam.name

        teamManager.add(newTeam)
        print "player_73行:新建队伍成员",newTeam.member
        print "player_78行:玩家.team.member:",self.team.member
        gwdata.drawTeamMember(self)
        playerManager.add(self)


    def c2gsInvited(self,invitee):
        packet = send_packet.SendPacket(8)
        packet.packString(invitee.name)
        print "C 队长 发出 邀请 包 ,被邀请者 -->期待 str name:", invitee.name
        packet.send()
        print "发送邀请请求"
    def inviteAskShow(self,inviterName):
        gwdata.inviteAskShow(self,inviterName)
    def c2gsInviteReply(self,answer,inviterName):
        packet = send_packet.SendPacket(9)
        packet.packString(answer)
        packet.packString(inviterName)
        packet.send()
    def inviteAnswerReply(self):
        gwdata.inviteAnswerReply(self)

    def c2gsKickOut(self,playerUnderMouse):
        memberName = playerUnderMouse.name
        packet = send_packet.SendPacket(10)
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
        packet = send_packet.SendPacket(11)
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
        packet = send_packet.SendPacket(12)
        packet.packString(playerUnderMouse.name)
        packet.send()
    def joinIn(self,newMemberName):
        self.team = teamManager.getByTeamName(self)
        self.team.add(newMemberName)
        teamManager.add(self.team)
        gwdata.drawTeamMember(self)
    def c2gsQuitTeam(self,playerUnderMouse):
        packet = send_packet.SendPacket(13)
        packet.send()
        print "发生退伍请求:"




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
    playerToExit =playerManager.remotePlayers[name]
    playerToExit.exitGame()
def gs2cTeamCreate(player,packet):
    player.teamCreate()
def gs2cOtherTeamCreate(player,packet):
    playerName = packet.unpackString()
    teamName= packet.unpackString()
    playerGeted = playerManager.get(playerName)
    newTeam = team.Team()
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
    inviter = playerManager.get(inviterName)
    invitee = playerManager.get(inviteeName)

    if answer == "Yes":
        if player.name == inviteeName: #这个玩家是被邀请者
            print "#这个玩家是被邀请者"
            newTeam = team.Team()
            newTeam.create(inviter)
            player.team = newTeam
            for i in range(memberNum):
                memberName = packet.unpackString()
                print "被邀请者,通过邀请者,创建队伍,并添加所有队员(含自己)"
                player.team.add(memberName)
                member = playerManager.get(memberName)
                print "初始化所有队友的右键菜单"
                menu.Menu([],member)
                member.menu.updateMenuOption([7])
                playerManager.add(member)
            menu.Menu([],player)
            player.menu.updateMenuOption([6])# 退出队伍
            menu.Menu([],inviter)
            inviter.menu.updateMenuOption([8])# 显示" isMyCaption

            playerManager.add(player)
            teamManager.add(newTeam)
            playerManager.add(inviter)
        elif player.name == inviterName:
            print "这个玩家是队长,邀请者"
            player.team = teamManager.getByTeamName(player)
            player.team.add(inviteeName) #
            invitee.menu.updateMenuOption([2,3])# 转让队长,踢掉玩家

            teamManager.add(player.team)
            playerManager.add(player)
            playerManager.add(invitee)
        else:
            player.team.add(inviteeName)
            playerManager.add(player)
            teamManager.add(player.team)
            menu.Menu([],invitee)
            invitee.menu.updateMenuOption([7])
        player.inviteAnswerReply()

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
    if player.name == memberName:
        player.team=""
        playerManager.add(player)
        gwdata.disDrawTeamMember()
    else:
        player.team.remove(memberName)
        gwdata.drawTeamMember(player)
