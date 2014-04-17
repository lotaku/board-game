#!/usr/bin/env python
# encoding: utf-8
from player_manager import playerManager
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

    #if answer == "Yes":
        #if player.name == inviteeName: #这个玩家是被邀请者
            #print "#这个玩家是被邀请者"
            #newTeam = team.Team()
            #newTeam.create(inviter)
            #player.team = newTeam
            #for i in range(memberNum):
                #memberName = packet.unpackString()
                #print "被邀请者,通过邀请者,创建队伍,并添加所有队员(含自己)"
                #player.team.add(memberName)
                #member = playerManager.get(memberName)
                #print "初始化所有队友的右键菜单"
                #menu.Menu([],member)
                #member.menu.updateMenuOption([7])
                #playerManager.add(member)
            #menu.Menu([],player)
            #player.menu.updateMenuOption([6])# 退出队伍
            #menu.Menu([],inviter)
            #inviter.menu.updateMenuOption([8])# 显示" isMyCaption

            #playerManager.add(player)
            #teamManager.add(newTeam)
            #playerManager.add(inviter)
        #elif player.name == inviterName:
            #print "这个玩家是队长,邀请者"
            #player.team = teamManager.getByTeamName(player)
            #player.team.add(inviteeName) #
            #invitee.menu.updateMenuOption([2,3])# 转让队长,踢掉玩家

            #teamManager.add(player.team)
            #playerManager.add(player)
            #playerManager.add(invitee)
        #else:
            #player.team.add(inviteeName)
            #playerManager.add(player)
            #teamManager.add(player.team)
            #menu.Menu([],invitee)
            #invitee.menu.updateMenuOption([7])
        #player.inviteAnswerReply()

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
