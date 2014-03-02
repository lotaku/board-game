#!/usr/bin/env python
# encoding: utf-8
import pygame
import sys
#from player import player
import player
from pygame.locals import *
from player_manager import playerManager
import time
from team import team
from team_manager import teamManager


EXITKEY=0
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

MENUCURRENT ={}
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
HAVE_DRAW_TEAM_MEMBER =0
def loginWin():
    global DISPLAYSURF, player,FONT_OBJ,localPlayerName,LOCAL_PLAYER#team ,teamManager
    pygame.init()
    #FPSCLOCK=pygame.time.Clock()
    FONT_OBJ = pygame.font.Font('freesansbold.ttf', 22)
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
                playerManager.add(player.player)
                localPlayerName=player.player.name
                LOCAL_PLAYER=player.player
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
    global EXITKEY,MENUCURRENT,MENUCURRENT_KEY,LOCAL_PLAYER
    #print '所有玩家',playerManager.remotePlayers
    LOCAL_PLAYER = playerManager.get(localPlayerName)
    mousex = 0
    mousey = 0
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            player.player.c2gsExitGame()
            EXITKEY=1
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
        elif event.type == MOUSEBUTTONDOWN and not len(MENUCURRENT):
            #玩家左击移动
            if event.button == 1:
                mousex,mousey = event.pos
                boxx,boxy = getBoxAtPixel(mousex,mousey)
                if boxx !=None and boxy != None:
                    player.player.c2gsPlayerMove(boxx,boxy)
            if event.button == 3:  # 鼠标右击,判断是否画出右键菜单
                global LastBoxx,LastBoxy
                mousex,mousey = event.pos
                boxx,boxy = getBoxAtPixel(mousex,mousey)
                if boxx != None and boxy != None:
                    #LOCAL_PLAYER=playerManager.get(LOCAL_PLAYER.name)
                    #判断x,y 是否有玩家,并取得该玩家
                    for _,playerUnderMouse in playerManager.remotePlayers.items():
                        #print type(playerUnderMouse)
                        print "人物的X:",playerUnderMouse.x
                        if playerUnderMouse.x == LOCAL_PLAYER.x and playerUnderMouse.y == LOCAL_PLAYER.y:#右击player A 自己
                            print '右键下是本人'
                            #全功能菜单,初始化
                            menuRightAll={
                                    0:("TeamCreat",player.player.c2gsTeamCreate),\
                                    1:("Invited","def1"),\
                                    2:("kickedOut","def2"),\
                                    3:("transferCaptain","def3"),\
                                    4:("applyInto","def4"),\
                                    5:("disband",player.player.c2gsTeamCreate),\
                                        }
                            #player:是本地玩家 A ,playerundermouse 右键下的玩家 B
                            #if playerUnderMouse.x == player.player.x and playerUnderMouse.y == player.player.y:#右击player A 自己
                            LOCAL_PLAYER = playerManager.get(localPlayerName)
                            if LOCAL_PLAYER.iscaption:
                            #if 1==1:
                                #global MENUCURRENT_KEY
                                print "画 解散队伍"
                                MENUCURRENT_KEY=[5]
                                print '菜单字典 所有 keys:',
                                print MENUCURRENT_KEY
                                for key in MENUCURRENT_KEY:
                                    print "菜单字典的 key:",key
                                    MENUCURRENT[key]=menuRightAll[key]
                                LastBoxx,LastBoxy= drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy)
                            else:
                                print "画 创建队伍"
                                MENUCURRENT_KEY=[0]
                                print '菜单字典 所有 keys:',
                                print MENUCURRENT_KEY
                                for key in MENUCURRENT_KEY:
                                    print "菜单字典的 key:",key
                                    MENUCURRENT[key]=menuRightAll[key]
                                print "菜单k:v  ",MENUCURRENT
                                LastBoxx,LastBoxy= drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy)
                            #else:#不是本人 player A
                                ##判断两个玩家是否有一个队伍
                                ##localPlayerTeam = teamManager.get(player.player)
                                ##playerUnderMouseTeam  = teamManager.get(playerUnderMouse)
                                #if player.player.iscaption: # A 是队长
                                    #if playerUnderMouse.iscaption: #B 是队长
                                        #print '都是队长功能待定'
                                    #elif playerUnderMouse.name in localPlayerTeam.member:
                                        ## B不是队长,并且在A 的队伍里
                                        #print '获得当前右键菜单'
                                        #for i in [2,3]:
                                            #MENUCURRENT[i]=menuRightAll[i]
                                        #LastBoxx,LastBoxy= drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy)
                                #else:#player 不是队长
                                    #if playerUnderMouse.iscaption:#B 是队长
                                        #print "画 解散队伍"
                                        #MENUCURRENT[5]=menuRightAll[5]
                                        #LastBoxx,LastBoxy= drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy)
                                    #else:#B 不是队长
                                        #print "画 创建队伍"
                                        #MENUCURRENT[0]=menuRightAll[0]
                                        #LastBoxx,LastBoxy= drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy)

        elif event.type == MOUSEBUTTONDOWN and len(MENUCURRENT):
            if event.button == 1:
                mousex,mousey = event.pos
                MENUCURRENT = mouseLClickOnCurrentMenu(MENUCURRENT_KEY,MENUCURRENT, LastBoxx,LastBoxy,mousex,mousey)

def exitGame():
    if EXITKEY:
        #time.sleep(3)
        pygame.QUIT
        sys.exit()
def mouseRClick():
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:  # 鼠标右击
                #testFont= FONT_OBJ.render('xxx', True, NAVYBLUE)
                testFont = makeText("xxx",10,10)
                DISPLAYSURF.blit(testFont, (10,10))
def makeText(text,color,bgcolor,top,left):
    """返回 textSurf,textRect"""
    FONT_OBJ= pygame.font.Font('freesansbold.ttf', 22)
    textSurf=FONT_OBJ.render(text,True,color,bgcolor)
    textRect=textSurf.get_rect()
    textRect.topleft=(top,left)
    return (textSurf,textRect)

def drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy):
    """
    右击,判断用户属性,画出对应的右键菜单
    :return: menuCurrent,LastBoxx,LastBoxy
    """
    #画出菜单背景
    LastBoxx,LastBoxy = boxx,boxy
    left,top = leftTopCoordsOfBox(boxx+1, boxy)
    width =BOXSIZE
    height=BOXSIZE*2+GAPSIZE
    menuLineRect = pygame.draw.rect(DISPLAYSURF,RED,(left,top,width,height))
    lenght= range(len(MENUCURRENT_KEY))
    tempDict=zip(MENUCURRENT_KEY,lenght)
    print tempDict
    #for key,i in MENUCURRENT_KEY,lenght:
    for key,i in tempDict:
        print '画菜单'
        menuLineHeight = BOXSIZE/2
        menuLineSurf,menuLineRect = makeText(MENUCURRENT[key][0],WHITE,BGCOLOR,left,top+menuLineHeight*i)
        DISPLAYSURF.blit(menuLineSurf,menuLineRect)
    return LastBoxx,LastBoxy
def mouseLClickOnCurrentMenu(MENUCURRENT_KEY,menuCurrent, LastBoxx,LastBoxy,mousex,mousey):
    """
    鼠标点击在右键菜单上"""
    left,top = leftTopCoordsOfBox(LastBoxx+1, LastBoxy)
    width =BOXSIZE
    height=BOXSIZE*2+GAPSIZE
    menuRect = pygame.Rect(left,top,width,height)
    if menuRect.collidepoint(mousex,mousey):
        for i in MENUCURRENT_KEY:
            menuLineHeight = BOXSIZE/2
            _,menuLineRect = makeText(menuCurrent[i][0],WHITE,BGCOLOR,left,top+menuLineHeight*i)
            if menuLineRect.collidepoint(mousex,mousey):
                #testDef(menuCurrent[i][0])
                menuCurrent[i][1]()
                #print 'xxx',player.team.member
                #pygame.time.wait(3000)
    #重画菜单后面的背景+人物

    for _,playerBehindRMenu in playerManager.remotePlayers.items():
        for i in [1,2]:# 两行
            for j in [1,2]: #两列
                if playerBehindRMenu.x == left and  playerBehindRMenu.y == top:
                    drawPlayer(playerBehindRMenu)
                    left +=1*(j-1)
                    top  +=1*(i-1)

    #清空右键菜单
    MENUCURRENT={}
    return MENUCURRENT
def drawTeamMember():
    #global HAVE_DRAW_TEAM_MEMBER
    #if not HAVE_DRAW_TEAM_MEMBER:
    print '成员数,',len(player.team.member)
    for memberName in player.team.member:
        for i in range(len(player.team.member)):
            memberSurf,memberRect = makeText(memberName,RED,GREEN,20+(66*i),20)
            DISPLAYSURF.blit(memberSurf,memberRect)
        #HAVE_DRAW_TEAM_MEMBER = 1


def testDef(text):
    testFont,testRect = makeText(text,RED,BGCOLOR,10,10)
    DISPLAYSURF.blit(testFont, testRect)













