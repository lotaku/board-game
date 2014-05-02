#!/usr/bin/env python
# encoding: utf-8
import sys
import os
import pygame
from game_win import gameWin
path=os.path.abspath("../../")
#print '绝对路径：',path
sys.path.insert(1,path)
#print sys.path
class GameWorld():
    def __init__(self):
        #gameWin.displaySurf.fill(bgcolor)
        self.BOXCOLOR = (255, 255, 255) #WHITE
        self.BOXSIZE=85
        self.GAPSIZE=10
        self.BOARDWIDTH =6
        self.BOARDHEIGHT = 4
        #print "gameWin 模块的属性：",dir(gameWin)
        self.XMARGIN = int((gameWin.WINDOWWIDTH - (self.BOARDWIDTH* (self.BOXSIZE + self.GAPSIZE))) / 2)
        self.YMARGIN = int((gameWin.WINDOWHEIGHT - (self.BOARDHEIGHT * (self.BOXSIZE + self.GAPSIZE))) / 2)
        #                R    G    B
        self.GRAY     = (100, 100, 100)
        self.NAVYBLUE = ( 60,  60, 100)
        self.WHITE    = (255, 255, 255)
        self.RED      = (255,   0,   0)
        self.GREEN    = (  0, 255,   0)
        self.BLUE     = (  0,   0, 255)
        self.YELLOW   = (255, 255,   0)
        self.ORANGE   = (255, 128,   0)
        self.PURPLE   = (255,   0, 255)
        self.CYAN     = (  0, 255, 255)

        self.FONT_COLOR     = self.RED
        self.BGCOLOR        = self.NAVYBLUE
        self.LIGHTBGCOLOR   = self.GRAY
        self.BOXCOLOR       = self.WHITE
        self.HIGHLIGHTCOLOR = self.BLUE
        self.HAVE_DRAW_TEAM_MEMBER = 0
        self.boyImg  = pygame.image.load('../../boy.png')
        self.girlImg = pygame.image.load("../../catgirl.png")
    def createMap(self):
        gameWin.displaySurf.fill(self.BGCOLOR)
        for boxx in range(self.BOARDWIDTH):
            for boxy in range(self.BOARDHEIGHT):
                left, top = self.leftTopCoordsOfBox(boxx, boxy)
                pygame.draw.rect(gameWin.displaySurf, self.BOXCOLOR,(left, top, self.BOXSIZE, self.BOXSIZE))

    def leftTopCoordsOfBox(self, boxx, boxy):
        left = boxx * (self.BOXSIZE + self.GAPSIZE) + self.XMARGIN
        top = boxy * (self.BOXSIZE + self.GAPSIZE) + self.YMARGIN
        return (left, top)
    def getBoxAtPixel(self,x, y):
        for boxx in range(self.BOARDWIDTH):
            for boxy in range(self.BOARDHEIGHT):
                left, top = self.leftTopCoordsOfBox(boxx, boxy)
                boxRect = pygame.Rect(left, top, self.BOXSIZE, self.BOXSIZE)
                if boxRect.collidepoint(x, y):
                    return (boxx, boxy)
        return (None, None)

    #def showRClickMenu(keyList):
        #"""显示指定菜单"""
        #global MENUCURRENT,menuRightAll,LastBoxx,LastBoxy,boxx,boxy,MENUCURRENT_KEY

        #MENUCURRENT_KEY=keyList
        #for key in MENUCURRENT_KEY:
            #MENUCURRENT[key]=menuRightAll[key]
        #LastBoxx,LastBoxy= drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy)

    def reImport_player(self):
        import player
        print "重新import player 获得 localplayer：",player.localPlayer
        return player
gameWorld = GameWorld()
