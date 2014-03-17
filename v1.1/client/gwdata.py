#!/usr/bin/env python
# encoding: utf-8
import pygame
import sys
import player
from pygame.locals import K_ESCAPE,QUIT,KEYUP,K_RETURN,MOUSEBUTTONDOWN
from player_manager import playerManager
import gwElements
from gwElements.game_Win import gameWin
from gwElements.game_world import gameWorld

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

# 初始化某些类
#玩家自己

class MakeFont():

    def __init__(self,text,top,left):
        """返回 textSurf,textRect"""
        RED      = (255,   0,   0)
        NAVYBLUE = ( 60,  60, 100)
        self.color   = RED
        self.bgcolor = NAVYBLUE
        self.text=text
        self.topleft=(top,left)
        self.make()

    def make(self):
        fontObj= pygame.font.Font('freesansbold.ttf', 22)
        textSurf=fontObj.render(self.text,True,self.color,self.bgcolor)
        textRect=textSurf.get_rect()
        textRect.topleft=self.topleft
        self.textSurf=textSurf
        self.textRect=textRect

#class GameWin():
    #def __init__(self):
        #self.WINDOWWIDTH=680
        #self.WINDOWHEIGHT=580
        #self.caption="Board Game"
        #self.bgcolor=(60, 60, 100)
    #def play(self):
        #pygame.init()
        #pygame.display.set_caption(self.caption)
        #self.displaySurf=pygame.display.set_mode((self.WINDOWWIDTH,self.WINDOWHEIGHT))
        #self.displaySurf.fill(self.bgcolor)

#gameWin=GameWin()
class ClientRender():
    def __init__(self):
        self.fps=30
        self.fpsClock= pygame.time.Clock()

    def render(self):
        pygame.display.update()
        self.fpsClock.tick(self.fps)

clientRender=ClientRender()

class FontObj():
    """返回 text 对应的 self.textSurf 对象"""
    def __init__(self,text):
        self.fontSize = 22
        self.font = "freesansbold.ttf"
        self.text=text
        self.color = (255,   0,   0) #RED
        self.bgcolor = ( 60,  60, 100)#NAVYBLUE
        self.makeFontObj()

    def makeFontObj(self):
        #pygame.init()
        fontObj = pygame.font.Font(self.font,self.fontSize)
        self.textSurf = fontObj.render(self.text,True,self.color,self.bgcolor)


class ShowHint():
    def __init__(self):
        self.color = (  0, 255,   0)#GREEN
        self.bgcolor =( 60,  60, 100)#NAVYBLUE
        self.fontSize = 22
        self.font = "freesansbold.ttf"
    def updateText(self,text,coordinates):
        self.text = text
        self.coordinates = coordinates
        fontObj = FontObj(self.text)
        self.textSurf= fontObj.textSurf
    def blit(self):
        gameWin.displaySurf.blit(self.textSurf, self.coordinates)



print dir(player)
print player.__name__
print player.__doc__
print player.__file__
class LoginWin():
    def __init__(self):
        pass

    def loop(self):
        self.hint_enterYourName = ShowHint()
        self.hint_enterYourName.updateText('Enter Your UserName (Submit with "ENTER" key)',(50,80))
        self.hint_enterYourName.blit()
        while True:
            breakKey=0
            for event in pygame.event.get():
                if event.type == QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key != K_RETURN:
                    self.enterPlayerName(player.localPlayer,event)
                elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                    print "commit something..."
                    player.localPlayer.c2gsEnterWorld()
                    breakKey=1
            if breakKey:
                break
            clientRender.render()
    def createAnewPlayer(self):
        from player import Player
        return Player()

    def enterPlayerName(self,playerArgm,event):
        playerArgm.name += event.unicode
        localPlayerNameText = FontObj(playerArgm.name)
        gameWin.displaySurf.blit(localPlayerNameText.textSurf,(255,200))


loginWin=LoginWin()


#class GameWorld():
    #def __init__(self):
        ##gameWin.displaySurf.fill(bgcolor)
        #self.BOXCOLOR = (255, 255, 255) #WHITE
        #self.BOXSIZE=85
        #self.GAPSIZE=10
        #self.BOARDWIDTH =6
        #self.BOARDHEIGHT = 4
        #print "gameWin 模块的属性：",dir(gameWin)
        #self.XMARGIN = int((gameWin.WINDOWWIDTH - (self.BOARDWIDTH* (self.BOXSIZE + self.GAPSIZE))) / 2)
        #self.YMARGIN = int((gameWin.WINDOWHEIGHT - (self.BOARDHEIGHT * (self.BOXSIZE + self.GAPSIZE))) / 2)
        ##                R    G    B
        #self.GRAY     = (100, 100, 100)
        #self.NAVYBLUE = ( 60,  60, 100)
        #self.WHITE    = (255, 255, 255)
        #self.RED      = (255,   0,   0)
        #self.GREEN    = (  0, 255,   0)
        #self.BLUE     = (  0,   0, 255)
        #self.YELLOW   = (255, 255,   0)
        #self.ORANGE   = (255, 128,   0)
        #self.PURPLE   = (255,   0, 255)
        #self.CYAN     = (  0, 255, 255)

        #self.FONT_COLOR            = RED
        #self.BGCOLOR               = NAVYBLUE
        #self.LIGHTBGCOLOR          = GRAY
        #self.BOXCOLOR              = WHITE
        #self.HIGHLIGHTCOLOR        = BLUE
        #self.HAVE_DRAW_TEAM_MEMBER = 0
        #self.girlImg               = pygame.image.load("../catgirl.png")
        #self.boyImg                = pygame.image.load('../boy.png')
    #def createMap(self):
        #gameWin.displaySurf.fill(self.BGCOLOR)
        #for boxx in range(gameWorld.BOARDWIDTH):
            #for boxy in range(gameWorld.BOARDHEIGHT):
                #left, top = self.leftTopCoordsOfBox(boxx, boxy)
                #pygame.draw.rect(gameWin.displaySurf, self.BOXCOLOR,(left, top, self.BOXSIZE, self.BOXSIZE))

    #def leftTopCoordsOfBox(self, boxx, boxy):
        #left = boxx * (self.BOXSIZE + self.GAPSIZE) + self.XMARGIN
        #top = boxy * (self.BOXSIZE + self.GAPSIZE) + self.YMARGIN
        #return (left, top)
    #def getBoxAtPixel(self,x, y):
        #for boxx in range(gameWorld.BOARDWIDTH):
            #for boxy in range(gameWorld.BOARDHEIGHT):
                #left, top = gameWorld.leftTopCoordsOfBox(boxx, boxy)
                #boxRect = pygame.Rect(left, top, gameWorld.BOXSIZE, gameWorld.BOXSIZE)
                #if boxRect.collidepoint(x, y):
                    #return (boxx, boxy)
        #return (None, None)

    #def showRClickMenu(keyList):
        #"""显示指定菜单"""
        #global MENUCURRENT,menuRightAll,LastBoxx,LastBoxy,boxx,boxy,MENUCURRENT_KEY

        #MENUCURRENT_KEY=keyList
        #for key in MENUCURRENT_KEY:
            #MENUCURRENT[key]=menuRightAll[key]
        #LastBoxx,LastBoxy= drawCurrentMenu(MENUCURRENT_KEY,MENUCURRENT,boxx,boxy)

    #def reImport_player(self):
        #import player
        #print "重新import player 获得 localplayer：",player.localPlayer
        #return player

#gameWorld=GameWorld()

class Draw():
    def __init__(self):
        pass
    def drawPlayer(self,playerArgm):
        """地图每个格式也都有属性，比如谁在那里。"""
        # 画一个格子
        left, top = gameWorld.leftTopCoordsOfBox(playerArgm.x,playerArgm.y)
        pygame.draw.rect(gameWin.displaySurf, gameWorld.BOXCOLOR, (left, top, gameWorld.BOXSIZE, gameWorld.BOXSIZE))
        #画玩家图像
        gameWin.displaySurf.blit(girlImg, (left+20,top))
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
            menuLineSurf,menuLineRect = makeText(menuArgm.menuOption[key][0],WHITE,BGCOLOR,left,top+menuArgm.menuLineHeight*i)
            gameWorld.blit(menuLineSurf,menuLineRect)
            i+=1

draw=Draw()

class Menu():
    def __init__(self):
        pass
    def createRightMenu(self):
        import player
        menuOption={
                0:("TeamCreat",player.localPlayer.c2gsTeamCreate),
                1:("Invited",player.localPlayer.c2gsInvited),
                2:("kickedOut",player.localPlayer.c2gsKickOut),
                3:("TransferCaptain",player.localPlayer.c2gsTransferCaptain),
                4:("JionIn",player.localPlayer.c2gsJoinIn),
                5:("QuitTeam",player.localPlayer.c2gsQuitTeam),
                6:("Disband","def6"),
                    }
        self.menuOption=menuOption
        self.menuOptionLength= len(menuOption)

        self.menuOptionList = []
        print menuOption
        for key, _ in menuOption.items():
            self.menuOptionList.append(key)



rightMenu = Menu()
rightMenu.createRightMenu()



class PlayerAction():
    def __init__(self):
        pass

    def moveCapture(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                player.localPlayer.c2gsExitGame()
            elif event.type == MOUSEBUTTONDOWN :
                mousex,mousey = event.pos
                ##是否点包含在右键菜单内:
                #if event.button == 1 and len(MENUCURRENT):
                    #MENUCURRENT = mouseLClickOnCurrentMenu(playerUnderMouseArgm,MENUCURRENT_KEY,MENUCURRENT, LastBoxx,LastBoxy,mousex,mousey)
                    #continue
                #玩家左击移动
                if event.button == 1:
                    mousex,mousey = event.pos
                    boxx,boxy = gameWorld.getBoxAtPixel(mousex,mousey)
                    if boxx !=None and boxy != None:
                        player.localPlayer.c2gsPlayerMove(boxx,boxy)
                    #else:
                        #if len(askMenuDict):
                            #inviteAskReply(mousex,mousey)
                if event.button == 3:  # 鼠标右击,判断是否画出右键菜单
                    mousex,mousey = event.pos
                    boxx,boxy = gameWorld.getBoxAtPixel(mousex,mousey)
                    if boxx != None and boxy != None:
                        #判断x,y 是否有玩家,并取得该玩家
                        for _,playerUnderMouse in playerManager.remotePlayers.items():
                            if playerUnderMouse.x == boxx and playerUnderMouse.y == boxy:
                                #playerUnderMouseArgm = playerUnderMouse
                                draw.drawMenu(rightMenu,boxx,boxy)
playerAction= PlayerAction()

def erasePlayer(player):
    left, top = leftTopCoordsOfBox(player.x,player.y)
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

def drawBoxes(tupleList):
    for boxx,boxy in tupleList:
        left,top = leftTopCoordsOfBox(boxx,boxy )
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

def drawBgcolor(left,top,width,height):
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, width, height))
def drawPlayer(player):
    global DISPLAYSURF
    print "新的x：",player.x
    left, top = leftTopCoordsOfBox(player.x,player.y)
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    DISPLAYSURF.blit(girlImg, (left+20,top))
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    userNameSurfaceObj = fontObj.render(player.name, True, NAVYBLUE)
    DISPLAYSURF.blit(userNameSurfaceObj, (left+20,top+60))
    print "刷新测试："
    pygame.display.update()

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
    LOCAL_PLAYER = playerManager.get(localPlayerName)
    mousex = 0
    mousey = 0
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            player.player.c2gsExitGame()
            EXITKEY=1
        elif event.type == MOUSEBUTTONDOWN :
            mousex,mousey = event.pos
            #是否点包含在右键菜单内:
            if event.button == 1 and len(MENUCURRENT):
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
                mousex,mousey = event.pos
                boxx,boxy = getBoxAtPixel(mousex,mousey)
                if boxx != None and boxy != None:
                    #判断x,y 是否有玩家,并取得该玩家
                    for _,playerUnderMouse in playerManager.remotePlayers.items():
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
def exitGame():
    if EXITKEY:
        pygame.QUIT
        sys.exit()
def makeText(text,color,bgcolor,top,left):
    """返回 textSurf,textRect"""
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
    for key,i in tempDict:
        print '画菜单'
        menuLineHeight = BOXSIZE/2
        menuLineSurf,menuLineRect = makeText(MENUCURRENT[key][0],WHITE,BGCOLOR,left,top+menuLineHeight*i)
        DISPLAYSURF.blit(menuLineSurf,menuLineRect)
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
    boxylist = list(range(boxy,boxy+3))
    boxxlist = list(range(boxx,boxx+2))
    for boxy in boxylist:# 行
        for boxx in boxxlist: #列
            print "菜单后面的格子:",(boxx,boxy)
            drawBoxes([(boxx,boxy)])
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
def disDrawTeamMember():
    fillWithBGCOLOR(0,0,WINDOWWIDTH,YMARGIN)
def fillWithBGCOLOR(top,left,width,height):
    rect=pygame.Rect(top,left,width,height)
    pygame.draw.rect(DISPLAYSURF,BGCOLOR,rect)
    pygame.display.update()
    print "调用 fillWithBGCOLOR()"
def drawTeamMember(playerDraw):
    fillWithBGCOLOR(0,0,WINDOWWIDTH,YMARGIN)
    lenghtList = range(len(playerDraw.team.member))
    memberName = playerDraw.team.member
    print '成员数,',len(playerDraw.team.member)
    print '成员名:', memberName
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













