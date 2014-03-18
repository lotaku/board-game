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

    def drawMenu(self,menuArgm,boxx,boxy):
        """
        """
        #画出菜单背景
        left,top = gameWorld.leftTopCoordsOfBox(boxx+1, boxy)
        width    = gameWorld.BOXSIZE
        height   = gameWorld.BOXSIZE*3+gameWorld.GAPSIZE*2

        #菜单显示位置 和 大小
        menuArgm.positionAndSize = (left,top,width,height)
        #菜单背景 rect 对象
        menuArgm.bgRect = pygame.draw.rect(gameWin.displaySurf,gameWorld.RED,menuArgm.positionAndSize)
        #菜单选项高度
        menuArgm.menuLineHeight = gameWorld.BOXSIZE/2
        # 记录循环次数，用于计算 菜单选项的位置
        i=0
        for key in menuArgm.menuOptionList:
            print '画菜单'
            menuOption = menuArgm.menuOption[key][0]
            topNew     = top+menuArgm.menuLineHeight*i
            menuFontObj     = FontObj(menuOption)
            menuFontObj.changeTopleft(left,topNew)
            gameWin.displaySurf.blit(menuFontObj.textSurf,menuFontObj.textRect)
            i+=1

draw=Draw()
