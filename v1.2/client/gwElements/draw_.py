#!/usr/bin/env python
# encoding: utf-8
from game_world import gameWorld
from game_win import gameWin
from font_obj import FontObj
import pygame

class Draw():
    def __init__(self):
        pass
    def drawPlayer(self,playerArgm):
        """地图每个格式也都有属性，比如谁在那里。"""
        # 画一个格子
        left, top = gameWorld.leftTopCoordsOfBox(playerArgm.x,playerArgm.y)
        pygame.draw.rect(gameWin.displaySurf, gameWorld.BOXCOLOR, (left, top, gameWorld.BOXSIZE, gameWorld.BOXSIZE))
        #画玩家图像
        gameWin.displaySurf.blit(gameWorld.girlImg, (left+20,top))
        #画玩家名字
        userNameFontObj= FontObj(playerArgm.name)
        gameWin.displaySurf.blit(userNameFontObj.textSurf, (left+20,top+60))
        print "刷新测试："
        pygame.display.update()

    def erasePlayer(self,playerArgm):
        left, top = gameWorld.leftTopCoordsOfBox(playerArgm.x,playerArgm.y)
        pygame.draw.rect(gameWin.displaySurf, gameWorld.BOXCOLOR, (left, top, gameWorld.BOXSIZE, gameWorld.BOXSIZE))

    def drawMenu(self,menuArgm,playerArgm):
        """
        """
        menuArgm.ofPlayer = playerArgm
        #菜单的位置(以box坐标为单位距离，即地图的最小单位格子）：
        menuArgm.boxxlist = list(range(playerArgm.x,playerArgm.x+3)) #列
        menuArgm.boxylist = list(range(playerArgm.y,playerArgm.y+3)) #行
        #画出菜单背景
        self.left,self.top = gameWorld.leftTopCoordsOfBox(playerArgm.x+1, playerArgm.y)
        self.width    = (gameWorld.BOXSIZE+gameWorld.GAPSIZE)*2
        self.height   = (gameWorld.BOXSIZE+gameWorld.GAPSIZE)*3
        #菜单显示位置 和 大小 (像素坐标）
        menuArgm.positionAndSize = (self.left, self.top, self.width, self.height)
        #菜单背景 rect 对象
        menuArgm.bgRect = pygame.draw.rect(gameWin.displaySurf,gameWorld.RED,menuArgm.positionAndSize)
        #菜单选项高度
        menuArgm.menuLineHeight = gameWorld.BOXSIZE/2
        # 记录循环次数，用于计算 菜单选项的位置
        i=0
        # 用于记住 菜单选项的key，rect
        menuArgm.menuOptionRects={}
        for key in menuArgm.menuOptionList:
            print '画菜单'
            menuOption  = menuArgm.menuOption[key][0]
            topNew      = self.top+menuArgm.menuLineHeight*i
            menuFontObj = FontObj(menuOption)
            menuFontObj.changeTopleft(self.left,topNew)
            gameWin.displaySurf.blit(menuFontObj.textSurf,menuFontObj.textRect)
            menuArgm.menuOptionRects[key] = menuFontObj.textRect
            i+=1

        #菜单已经显示
        menuArgm.isShowing=1

    def disDrawMenu(self,menuArgm):
        print "#重画菜单后面的背景+人物"
        self.drawBgcolor(self.left, self.top,self.width,self.height)
        for boxy in menuArgm.boxylist:# 行
            for boxx in menuArgm.boxxlist: #列
                #重画 地图 最小单位 （Map Unit）
                self.drawBoxes([(boxx,boxy)])
                from player_manager import playerManager
                for _,playerGeted in playerManager.players.items():
                    if playerGeted.x == boxx and  playerGeted.y == boxy:
                        self.drawPlayer(playerGeted)
        #菜单状态：没有显示
        menuArgm.isShowing=0

    def drawBgcolor(self,left,top,width,height):
        pygame.draw.rect(gameWin.displaySurf, gameWorld.BGCOLOR, (left, top, width, height))
    def drawBoxes(self,tupleList):
        # 画格子
        for boxx,boxy in tupleList:
            left, top = gameWorld.leftTopCoordsOfBox(boxx,boxy)
            pygame.draw.rect(gameWin.displaySurf, gameWorld.BOXCOLOR, (left, top, gameWorld.BOXSIZE, gameWorld.BOXSIZE))
    def drawTeamMember(self,teamArgm):
        """画出队伍成员"""
        #画背景颜色
        self.drawBgcolor(0,0,gameWin.WINDOWWIDTH,gameWorld.YMARGIN)
        #画 队伍首个成员名字,的起始位置
        teamArgm.topOfmemberName=20
        teamArgm.leftOfmemberName=20
        teamArgm.nameGap=20
        i=1 # 用于递增 名字间的间隔
        for member in teamArgm.member:
            memberFontObj=FontObj(member.name)
            top = teamArgm.topOfmemberName
            left = teamArgm.leftOfmemberName+teamArgm.nameGap*(i-1)
            memberFontObj.changeTopleft(left,top)
            gameWin.displaySurf.blit(memberFontObj.textSurf,memberFontObj.textRect)
            if member.iscaption:
                text        = "Caption is :" + member.name
                textFontObj = FontObj(text)
                top  = teamArgm.topOfmemberName
                left = teamArgm.leftOfmemberName+20
                textFontObj.changeTopleft(top,left)
                gameWin.displaySurf.blit(textFontObj.textSurf,textFontObj.textRect)
            i+=1
    def disDrawTeamMember(self):
        self.drawBgcolor(0,0,gameWin.WINDOWWIDTH,gameWorld.YMARGIN)


draw=Draw()
