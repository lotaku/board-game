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
import menu


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
askMenuDict={}
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
FONT_COLOR=RED
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
                #LOCAL_PLAYER = player.Player()
                #LOCAL_PLAYER.c2gsEnterWorld()
                #playerManager.add(LOCAL_PLAYER)
                #localPlayerName=LOCAL_PLAYER.name
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

def drawBoxes(tupleList):
    for boxx,boxy in tupleList:
        left,top = leftTopCoordsOfBox(boxx,boxy )
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
        #pygame.draw.rect(DISPLAYSURF, RED, (left, top, BOXSIZE, BOXSIZE))

def drawBgcolor(left,top,width,height):
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, width, height))
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
    print "刷新测试："
    pygame.display.update()

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
    global EXITKEY,MENUCURRENT,MENUCURRENT_KEY,LOCAL_PLAYER,\
            askMenuDict,boxx,boxy,LastBoxx,LastBoxy,playerUnderMouse,\
            playerUnderMouseArgm

    #askMenuDict={}
    #print '所有玩家',playerManager.remotePlayers
    LOCAL_PLAYER = playerManager.get(localPlayerName)
    mousex = 0
    mousey = 0
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            player.player.c2gsExitGame()
            EXITKEY=1
        #elif event.type == MOUSEBUTTONDOWN and not len(MENUCURRENT):

        elif event.type == MOUSEBUTTONDOWN :
            mousex,mousey = event.pos
            #isCollidepoint = menuBgRect.collidepoint(mousex,mousey)
            #是否点包含在右键菜单内:
            #if event.button == 1 and isCollidepoint:
            if event.button == 1 and len(MENUCURRENT):
                #MENUCURRENT = mouseLClickOnCurrentMenu(playerUnderMouse,MENUCURRENT_KEY,MENUCURRENT, LastBoxx,LastBoxy,mousex,mousey)
                MENUCURRENT = mouseLClickOnCurrentMenu(playerUnderMouseArgm,MENUCURRENT_KEY,MENUCURRENT, LastBoxx,LastBoxy,mousex,mousey)
                continue

            #玩家左击移动
            if event.button == 1:
                mousex,mousey = event.pos
                boxx,boxy = getBoxAtPixel(mousex,mousey)
                if boxx !=None and boxy != None:
                    player.player.c2gsPlayerMove(boxx,boxy)
                else:
                    if len(askMenuDict):
                        inviteAskReply(mousex,mousey)
            if event.button == 3:  # 鼠标右击,判断是否画出右键菜单
                #global LastBoxx,LastBoxy
                mousex,mousey = event.pos
                boxx,boxy = getBoxAtPixel(mousex,mousey)
                if boxx != None and boxy != None:
                    #menuOpinion(LOCAL_PLAYER,boxx,boxy)
                    #LOCAL_PLAYER=playerManager.get(LOCAL_PLAYER.name)
                    #判断x,y 是否有玩家,并取得该玩家
                    #global playerUnderMouse
                    for _,playerUnderMouse in playerManager.remotePlayers.items():
                        #print type(playerUnderMouse)
                        #print "人物的X:",playerUnderMouse.x
                        if playerUnderMouse.x == boxx and playerUnderMouse.y == boxy:
                            playerUnderMouseArgm = playerUnderMouse
                            #全功能菜单,初始化
                            global menuRightAll
                            menuRightAll={
                                    0:("TeamCreat",player.player.c2gsTeamCreate),
                                    1:("Invited",player.player.c2gsInvited),
                                    2:("kickedOut",player.player.c2gsKickOut),
                                    3:("TransferCaptain",player.player.c2gsTransferCaptain),
                                    4:("JionIn",player.player.c2gsJoinIn),
                                    5:("QuitTeam",player.player.c2gsQuitTeam),
                                    6:("Disband","def6"),
                                    7:("isOtherMember","def7"),
                                    8:("isMyCaption","def8"),
                                    9:("aCommonPlayer","def9"),
                                    10:("U,I,caption","def10"),
                                        }
                            menuOptionList = list(range(7))
                            print menuOptionList
                            menu.Menu(menuRightAll,playerUnderMouse)
                            playerUnderMouse.menu.updateMenuOption(menuOptionList)
                            playerUnderMouse.menu.showMenuOption()
###=============以下是根据玩家不同的状态显示的菜单,功能不完善,感觉太繁琐,暂时不弄===
                            #if playerUnderMouse.x == LOCAL_PLAYER.x and playerUnderMouse.y == LOCAL_PLAYER.y:#右击player A 自己
                                #print '右键下是本人'
                                #print playerUnderMouse.menu
                                #if not playerUnderMouse.menu:
                                    #print " 没有右键菜单, --> 菜单初始化"
                                    #menu.Menu(menuRightAll,playerUnderMouse)
                                    #playerUnderMouse.menu.updateMenuOption([0])
                                #print "显示右键菜单"
                                #playerUnderMouse.menu.showMenuOption()
                            #else:
                                #print "右键下不是A"
                                #if not playerUnderMouse.menu:
                                    #print "没有右键菜单, --> 菜单初始化 --> 右键下是个普通玩家"
                                    #menu.Menu(menuRightAll,playerUnderMouse)
                                    #LOCAL_PLAYER = playerManager.get(localPlayerName)
                                    #if LOCAL_PLAYER.iscaption:
                                        #print "a is caption:"

                                        #if playerUnderMouse.iscaption:
                                            #print 'b is caption'
                                            #playerUnderMouse.menu.updateMenuOption([10])
                                        #elif playerUnderMouse.teamName:
                                            #print 'b is a member'
                                            #playerUnderMouse.menu.updateMenuOption([7])
                                        #else:
                                            #print 'b is a common player'
                                            #playerUnderMouse.menu.updateMenuOption([1])

                                    #elif LOCAL_PLAYER.teamName:
                                        #print "a is a member"

                                        #if playerUnderMouse.iscaption:
                                            #print 'b is caption'
                                            ##playerUnderMouse.menu.updateMenuOption([1])
                                        #elif playerUnderMouse.teamName:
                                            #print 'b is a member'
                                            ##playerUnderMouse.menu.updateMenuOption([1])
                                        #else:
                                            #print 'b is a common player'
                                    #else:
                                        #print "a is common player"

                                        #if playerUnderMouse.iscaption:
                                            #print 'b is caption'
                                            #playerUnderMouse.menu.updateMenuOption([4])
                                        #elif playerUnderMouse.teamName:
                                            #print 'b is a member'
                                        #else:
                                            #print 'b is a common player'
                                            #playerUnderMouse.menu.updateMenuOption([0])
                                #print "显示右键菜单"
                                #playerUnderMouse.menu.showMenuOption()
def exitGame():
    if EXITKEY:
        #time.sleep(3)
        pygame.QUIT
        sys.exit()
def makeText(text,color,bgcolor,top,left):
    """返回 textSurf,textRect"""
    #FONT_OBJ= pygame.font.Font('freesansbold.ttf', 22)
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
    height=BOXSIZE*3+GAPSIZE*2
    global menuBgRect
    menuBgRect = pygame.draw.rect(DISPLAYSURF,RED,(left,top,width,height))
    lenght= range(len(MENUCURRENT_KEY))
    tempDict=zip(MENUCURRENT_KEY,lenght)
    print tempDict
    #for key,i in MENUCURRENT_KEY,lenght:
    for key,i in tempDict:
        print '画菜单'
        menuLineHeight = BOXSIZE/2
        menuLineSurf,menuLineRect = makeText(MENUCURRENT[key][0],WHITE,BGCOLOR,left,top+menuLineHeight*i)
        DISPLAYSURF.blit(menuLineSurf,menuLineRect)
    #return LastBoxx,LastBoxy,menuLineRect
    return LastBoxx,LastBoxy
def mouseLClickOnCurrentMenu(playerUnderMouse,MENUCURRENT_KEY,menuCurrent, LastBoxx,LastBoxy,mousex,mousey):
    """
    鼠标点击在右键菜单上"""
    left,top = leftTopCoordsOfBox(LastBoxx+1, LastBoxy)
    width =BOXSIZE
    height=BOXSIZE*3+GAPSIZE*3
    menuRect = pygame.Rect(left,top,width,height)
    if menuRect.collidepoint(mousex,mousey):
        lenght= range(len(MENUCURRENT_KEY))
        tempDict=zip(MENUCURRENT_KEY,lenght)
        print tempDict
        for key,i in tempDict:
            print "捕获右键 菜单 点击"
            menuLineHeight = BOXSIZE/2
            _,menuLineRect = makeText(menuCurrent[key][0],WHITE,BGCOLOR,left,top+menuLineHeight*i)
            if menuLineRect.collidepoint(mousex,mousey):
                #menuCurrent[i][1](playerUnderMouse)
                if key == 0:
                    print '调用创建队伍菜单'
                    menuCurrent[key][1]()
                else:
                    print "调用邀请菜单:",
                    print menuCurrent[key][1]
                    menuCurrent[key][1](playerUnderMouse)

    ##重画菜单后面的背景+人物
    reDrawPlayerBehindMenu(left,top,LastBoxx,LastBoxy)
    #清空右键菜单
    MENUCURRENT={}
    return MENUCURRENT
def reDrawPlayerBehindMenu(left,top,LastBoxx,LastBoxy):
    print "#重画菜单后面的背景+人物"
    width = (BOXSIZE+GAPSIZE)*2
    height =(BOXSIZE+GAPSIZE)*3
    drawBgcolor(left,top,width,height)
    boxx,boxy =  getBoxAtPixel(left,top)
    print 'left:',left
    print 'top:',top
    #boxx = LastBoxx+1
    #boxy = LastBoxy
    boxylist = list(range(boxy,boxy+3))
    boxxlist = list(range(boxx,boxx+2))
    for boxy in boxylist:# 行
        for boxx in boxxlist: #列
            print "菜单后面的格子:",(boxx,boxy)
            drawBoxes([(boxx,boxy)])
            #drawPlayer(LOCAL_PLAYER)
            for _,playerBehindRMenu in playerManager.remotePlayers.items():
                if playerBehindRMenu.x == boxx and  playerBehindRMenu.y == boxy:
                    print "菜单后面的玩家x,y"
                    print (playerBehindRMenu.x,playerBehindRMenu.y)
                    drawPlayer(playerBehindRMenu)

def inviteAskShow(player,inviterName_local):
    global inviterName
    inviterName = inviterName_local
    message = "Do you want to join in %s's team?" % inviterName
    print "格式化后的message:",message
    top = YMARGIN/2
    left = XMARGIN/4
    messageSurf,messageRect = makeText(message,FONT_COLOR,BGCOLOR,top,left)
    #按钮 NO 和 YES
    noSurf,noRect = makeText("No",FONT_COLOR,BGCOLOR,left,top)
    yesSurf,yesRect = makeText("Yes",FONT_COLOR,BGCOLOR,left+50,top)
    DISPLAYSURF.blit(messageSurf,messageRect)
    DISPLAYSURF.blit(noSurf,noRect)
    DISPLAYSURF.blit(yesSurf,yesRect)
    global askMenuDict
    askMenuDict={"No":noRect,"Yes":yesRect}
    print '显示邀请询问菜单'
def inviteAskReply(mousex,mousey):
    """
    """
    print "调用 inviteAskReply()"
    global askMenuDict,inviterName
    #判断鼠标位置,并调用对应函数
    for buttonString, buttonRect in askMenuDict.items():
        if buttonRect.collidepoint(mousex,mousey):
            print '已经点击回答'
            player.player.c2gsInviteReply(buttonString,inviterName)

    print "#在DISPLAYSURF上消除 message"
    fillWithBGCOLOR(0,0,WINDOWWIDTH,YMARGIN)
    print "#清空askMenuDict"
    askMenuDict={}
    #print "#在DISPLAYSURF上消除 message"
    #fillWithBGCOLOR(0,0,WINDOWWIDTH,YMARGIN)
def inviteAnswerReply (player):
    print "#先画背景,在画内容"
    print "本地玩家的名字:" ,
    print player.name
    print "本地玩家的队伍实例",
    print player.team

    fillWithBGCOLOR(0,0,BOARDWIDTH,YMARGIN)
    drawTeamMember(player)
def updatePlayer(player):
    playerUpdated = playerManager.get(player.name)
    return playerUpdated

#def inviteAnswerReply (LOCAL_PLAYER,answer,inviter,inviterName,invitee,inviteeName,memberNum):
    #if answer == "Yes":
        #if player.name == inviteeName: #这个玩家是被邀请者
            #newTeam = team.Team()
            #newTeam.create(inviter)
            #player.team = newTeam
            #for i in range(memberNum):
                #memberName = packet.unpackString()
                #player.team.add(memberName)

    #if answer == "Yes":
        #LOCAL_PLAYER = playerManager.get(localPlayerName)
        #LOCAL_PLAYER_team = teamManager.get(LOCAL_PLAYER)
        #LOCAL_PLAYER_team.add(inviteeName)
        #print "刚刚加入了新的成员,新的队伍成员:"
        #print LOCAL_PLAYER_team.member
        #LOCAL_PLAYER.team=LOCAL_PLAYER_team

        #print "#先画背景,在画内容"
        #print "本地玩家的名字:" ,
        #print LOCAL_PLAYER.name
        #print "本地玩家的队伍实例",
        #print LOCAL_PLAYER.team
        #teamManager.add(LOCAL_PLAYER_team)
        #playerManager.add(LOCAL_PLAYER)
        #fillWithBGCOLOR(0,0,BOARDWIDTH,YMARGIN)
        #drawTeamMember(LOCAL_PLAYER)
##还需要 回复S? 让队员更新? 还是前面就应该先更新了?
    #else:
        #print "答案是否"
def disDrawTeamMember():
    fillWithBGCOLOR(0,0,WINDOWWIDTH,YMARGIN)
def fillWithBGCOLOR(top,left,width,height):
    rect=pygame.Rect(top,left,width,height)
    #rect=pygame.Rect(top,left,200,300)
    pygame.draw.rect(DISPLAYSURF,BGCOLOR,rect)
    #pygame.draw.rect(DISPLAYSURF,BGCOLOR,(0,0,500,600))
    pygame.display.update()
    print "调用 fillWithBGCOLOR()"
def drawTeamMember(playerDraw):
    #global HAVE_DRAW_TEAM_MEMBER
    #if not HAVE_DRAW_TEAM_MEMBER:
    fillWithBGCOLOR(0,0,WINDOWWIDTH,YMARGIN)
    lenghtList = range(len(playerDraw.team.member))
    memberName = playerDraw.team.member

    print '成员数,',len(playerDraw.team.member)
    print '成员名:', memberName
    #for memberName in playerDraw.team.member:
        #for i in range(len(playerDraw.team.member)):
            #memberSurf,memberRect = makeText(memberName,RED,GREEN,20+(66*i),20)
            #DISPLAYSURF.blit(memberSurf,memberRect)
        #HAVE_DRAW_TEAM_MEMBER = 1
    tempDict = zip(memberName, lenghtList) #
    for memberName,i in tempDict:
        memberSurf,memberRect = makeText(memberName,RED,GREEN,20+(66*i),20)
        DISPLAYSURF.blit(memberSurf,memberRect)
        # 判断队长是谁
        member = playerManager.get(memberName)
        if member.iscaption:
            captionMsg = 'Caption: '+memberName
            memberSurf,memberRect = makeText(captionMsg,RED,GREEN,20+(66*i),50)
            DISPLAYSURF.blit(memberSurf,memberRect)
    pygame.display.update()
def showRClickMenu(keyList):
    """显示指定菜单"""
    global MENUCURRENT,menuRightAll,LastBoxx,LastBoxy,boxx,boxy,MENUCURRENT_KEY

    MENUCURRENT_KEY=keyList
    for key in MENUCURRENT_KEY:
        MENUCURRENT[key]=menuRightAll[key]
    LastBoxx,LastBoxy= drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy)

def freshLOCAL_PLAYER():
    global LOCAL_PLAYER,localPlayerName
    LOCAL_PLAYER = playerManager.get(localPlayerName)
def testDef(text):
    testFont,testRect = makeText(text,RED,BGCOLOR,10,10)
    DISPLAYSURF.blit(testFont, testRect)













