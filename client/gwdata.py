#!/usr/bin/env python
# encoding: utf-8
import pygame
import sys
#from player import player
import player
from pygame.locals import *
from player_manager import playerManager




FPS=30
WINDOWWIDTH = 680
WINDOWHEIGHT=580
BOXSIZE=85
GAPSIZE=10
BOARDWIDTH = 6
BOARDHEIGHT = 4
revealedBoxes = []
NOBODY = 'WOW'
usersNum = BOARDWIDTH * BOARDHEIGHT  # 计算可容纳的用户总数
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

BOXX_MOVE_TEMP = 999
BOXY_MOVE_TEMP = 999


girlImg = pygame.image.load("../catgirl.png")
boyImg = pygame.image.load('../boy.png')

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
FPSCLOCK=pygame.time.Clock()
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
def loginWin():
    global DISPLAYSURF, player
    pygame.init()
    #FPSCLOCK=pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

    pygame.display.set_caption("Board Game")
    DISPLAYSURF.fill(NAVYBLUE)
    showEnterHint()
    pygame.display.update()
    while True:
        breakKey=0
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key != K_RETURN:
                enterPlayerName(player.player,event)
                #enterPlayerName(player,event)
            elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                player.player.c2gsEnterWorld()
                breakKey=1
        if breakKey:
            break
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def showEnterHint():
    global DISPLAYSURF
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    wellcomSurfaceObj = fontObj.render('Enter Your UserName (Submit with "ENTER" key)', True, GREEN, NAVYBLUE)
    DISPLAYSURF.blit(wellcomSurfaceObj, (55,150))

def enterPlayerName(player,event):
    player.name += event.unicode
    fontObj = pygame.font.Font('freesansbold.ttf',22)
    playerNameSurf=fontObj.render(player.name,True,ORANGE,NAVYBLUE)
    DISPLAYSURF.blit(playerNameSurf,(255,200))

def initGameWorld():
    DISPLAYSURF.fill(BGCOLOR)
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))


def erasePlayer(player):
    left, top = leftTopCoordsOfBox(player.x,player.y)
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

def drawPlayer(player):
    global DISPLAYSURF
    print "新的x：",player.x
    left, top = leftTopCoordsOfBox(player.x,player.y)
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    #drawGirl(player)
    DISPLAYSURF.blit(girlImg, (left+20,top))
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    userNameSurfaceObj = fontObj.render(player.name, True, NAVYBLUE)
    DISPLAYSURF.blit(userNameSurfaceObj, (left+20,top+60))
    #print "刷新测试："
    #pygame.display.update()

def drawPlayerTemp(player,boxx,boxy):
    global BOXX_MOVE_TEMP,BOXY_MOVE_TEMP
    """
    鼠标移动时，显示英雄"""
    #消除上次临时显示的player
    left, top = leftTopCoordsOfBox(BOXX_MOVE_TEMP,BOXY_MOVE_TEMP)
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    #显示这次的临时player
    left, top = leftTopCoordsOfBox(boxx,boxy)
    #pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    #drawGirl(player)
    DISPLAYSURF.blit(girlImg, (left+20,top))
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    userNameSurfaceObj = fontObj.render(player.name, True, NAVYBLUE)
    DISPLAYSURF.blit(userNameSurfaceObj, (left+20,top+60))

    BOXX_MOVE_TEMP = boxx
    BOXY_MOVE_TEMP = boxy
def drawGirl(player):
    left, top = leftTopCoordsOfBox(player.x,player.y)
    DISPLAYSURF.blit(girlImg, (left+20,top))
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    userNameSurfaceObj = fontObj.render(player.name, True, NAVYBLUE)
    DISPLAYSURF.blit(userNameSurfaceObj, (left+20,top+60))

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)
def clientRender():
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def playermove():
    #DISPLAYSURF.fill(BGCOLOR)
    #mouseClicked = False
    mousex = 0
    mousey = 0
    #print "play函数，获取event"
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        #elif event.type == MOUSEMOTION:
            #mousex,mousey =event.pos
            #boxx,boxy = getBoxAtPixel(mousex,mousey)
            ##确定移动前，临时显示player
            #if boxx !=None and boxy != None:
                #for _,playerOther in playerManager.remotePlayers.items():
                    #x = playerOther.x
                    #y = playerOther.y
                    #if boxx != x or boxy != y:
                        ##print "调用drawPlaye"
                        #drawPlayerTemp(player.player,boxx,boxy)

        elif event.type == MOUSEBUTTONUP:
            mousex,mousey = event.pos
            boxx,boxy = getBoxAtPixel(mousex,mousey)
            #确定移动前，临时显示player
            if boxx !=None and boxy != None:
                player.player.c2gsPlayerMove(boxx,boxy)


