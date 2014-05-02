#!/usr/bin/env python
# encoding: utf-8
from font_obj import FontObj
from game_world import gameWorld
from blit import blit as blitINS
from rect_collection import rectCollection
class Invitation():
    def __ini__(self):
        pass
    def inviteAskShow(self,playerArgm,inviterName):
        from player import localPlayer
        """ top : 距离左边的距离
            left : 距离上报的距离
            应该是我前面设计错误。"""
        #显示区域的 起始点（像素坐标）
        top     = gameWorld.YMARGIN/4
        left    = gameWorld.XMARGIN
        #定义 邀请询问句及其显示位置
        message = "Do you want to join in %s's team?" % inviterName
        message = FontObj(message)
        message.changeTopleft(left,top)

        #定义按钮 NO 和 YES 及其显示位置
        yes = FontObj("Yes")
        yes.changeTopleft(left+150,top+30)
        # 这里yes.textRect 是unhashable 对象，不能作为字典的键值
        #                   #实例   #功能函数                   #参数
        rectCollection.rects[yes]=(localPlayer.c2gsInviteReply,(yes.text,inviterName))

        no  = FontObj("No")
        no.changeTopleft(left,top+30)
        rectCollection.rects[no]=(localPlayer.c2gsInviteReply,(no.text,inviterName))

        for fontObj in [message,no,yes]:
            blitINS.blitFont(fontObj)

        # idea --> 将每次创建的 具有某个函数功能的 rect:fun 集中到某个字典，每次捕获鼠标点击是，迭代该字典

    def inviteAnswerReply(self, answer, members, inviter, invitee):
        from player import localPlayer
        from team import Team
        from player_manager import playerManager
        from team_manager import teamManager
        from draw_ import draw

        if localPlayer.name is invitee.name:
            newTeam = Team()
            newTeam.create(inviter)
            for member in members:
                newTeam.add(member)
            #更新玩家和team 数据 idea-->定义一个“更新”类，用@classmethod？
            invitee.team = newTeam
            inviter.team = newTeam
            playerManager.add(inviter)
            playerManager.add(invitee)
            teamManager.add(newTeam)
            #画出队伍成员
            draw.disDrawTeamMember()
            draw.drawTeamMember(newTeam)
        elif localPlayer.name is inviter.name:
            inviter.team = teamManager.get(inviter)
            inviter.team.add(invitee)
            #更新玩家和team 数据
            playerManager.add(inviter)
            teamManager.add(inviter.team)
            #画出队伍成员
            draw.disDrawTeamMember()
            draw.drawTeamMember(inviter.team)
        else:# 其他队员
            localPlayer.team.add(invitee)
            #更新玩家和team 数据
            playerManager.add(localPlayer)
            teamManager.add(localPlayer.team)
            #画出队伍成员
            draw.disDrawTeamMember()
            draw.drawTeamMember(localPlayer.team)





invitation = Invitation()

