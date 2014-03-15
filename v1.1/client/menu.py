#!/usr/bin/env python
# encoding: utf-8
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
        playerUnderMouse.menu= self
    def updateMenuOption(self,menuOptionList):
        self.menuOptionList = menuOptionList
    def showMenuOption(self):
        if self.menuOptionList:
            gwdata.showRClickMenu(self.menuOptionList)
        else:
            print "没有定义合适的菜单选项"
