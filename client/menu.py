#!/usr/bin/env python
# encoding: utf-8
#import player
import gwdata
class Menu():
    def __init__(self,menuOption,playerUnderMouse):
        self.menuRightAll=menuOption # 类似下方的菜单字典
        #self.menuRightAll={
            #0:("TeamCreat",player.player.c2gsTeamCreate),
            #1:("Invited",player.player.c2gsInvited),
            #2:("kickedOut","def2"),
            #3:("transferCaptain","def3"),
            #4:("applyInto","def4"),
            #5:("disband","def5"),
            #6:("QuitTeam","def6")
        #}
        self.menuOptionList = []
        #self.player = playerUnderMouse
        playerUnderMouse.menu= self
    def updateMenuOption(self,menuOptionList):
        self.menuOptionList = menuOptionList
    def showMenuOption(self):
        if self.menuOptionList:
            gwdata.showRClickMenu(self.menuOptionList)
        else:
            print "没有定义合适的菜单选项"
    #def menuBoundTo(self,user):
        #user.menu=self




        #gwdata.showRClickMenu()
        #if playerUnderMouse.x == LOCAL_PLAYER.x and playerUnderMouse.y == LOCAL_PLAYER.y:#右击player A 自己
            #print '右键下是本人'
            ##player:是本地玩家 A ,playerundermouse 右键下的玩家 B
            ##if playerUnderMouse.x == player.player.x and playerUnderMouse.y == player.player.y:#右击player A 自己
            #LOCAL_PLAYER = playerManager.get(localPlayerName)
            #if LOCAL_PLAYER.team:# 在某个队伍里
                #if LOCAL_PLAYER.iscaption:#是队长
                    #showRClickMenu([5])# 显示右键菜单:解散队伍
                #else:#不是队长
                    #showRClickMenu([6]) # 显示退出队伍
            ##if LOCAL_PLAYER.iscaption:
                ##showRClickMenu([5])# 显示右键菜单:解散队伍
            #else: #不在任何队伍
                #showRClickMenu([0])# 显示右键菜单:创建队伍
