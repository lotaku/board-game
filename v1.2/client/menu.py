#!/usr/bin/env python
# encoding: utf-8
import gwdata
class Menu():
    def __init__(self):
        pass
    def creat(self,menuOption):
        """DEMO:
        menuOption = {
            0:("TeamCreat",player.player.c2gsTeamCreate),
            1:("Invited",player.player.c2gsInvited),
        }
"""
        self.menuOption=menuOption
        self.menuRightAll=menuOption
        self.menuOptionList = []
    def updateMenuOption(self,menuOptionList):
        self.menuOptionList = menuOptionList
    def showMenuOption(self):
        gwdata.showRClickMenu(self.menuOptionList)
        #if self.menuOptionList:
            #gwdata.showRClickMenu(self.menuOptionList)
        #else:
            #print "没有定义合适的菜单选项"
