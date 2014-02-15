#!/usr/bin/env python
# encoding: utf-8
import random,\
        pygame,\
        sys,\
        socket,\
        struct,\
        time,\
        copy

from SocketServer import UDPServer, \
        DatagramRequestHandler, \
        ForkingMixIn, \
        BaseRequestHandler #, ForkingUDPServer

from pygame.locals import *
#import pygame.locals

FPS=30
WINDOWWIDTH = 680
WINDOWHEIGHT=580
BOXSIZE=85
GAPSIZE=10
BOARDWIDTH = 2
BOARDHEIGHT = 2
revealedBoxes = []
NOBODY = 'WOW'
usersNum = BOARDWIDTH * BOARDHEIGHT  # 计算可容纳的用户总数
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)


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

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
userName = ''
host = ''
port = 51423
serverAddr = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
board = []
def main():
    global FPSCLOCK, DISPLAYSURF,catImg,boyImg,userName#,revealedBoxes

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Board Game')
    DISPLAYSURF.fill(NAVYBLUE)

    revealedBoxes= generateRevealedBoxesData(False)

    pygame.display.update()

    while True:#login windows
        global userName,closeLoginWindow
        closeLoginWindow = False
        showEnterHint()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key != K_RETURN and event.key != K_ESCAPE: # K_KP_ENTER
                EnterUserName(event)
            elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                board = getRandomizedBoard()
                board, closeLoginWindow = enterWorld(userName)

        if closeLoginWindow:
            break
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    #justLogin = 1
    #initUserLocation(justLogin, revealedBoxes)

    while True: #Game Start
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)
        catImg = pygame.image.load('catgirl.png')
        boyImg = pygame.image.load('boy.png')
        showWellcomUser(userName)
        board = refreshWorld()
        drawBoard(board)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                exitWorld(userName)
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex,mousey =event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if board[boxx][boxy][0][0] == 'WOW':
                drawHighlightBox(boxx, boxy)
            if board[boxx][boxy][0][0] == 'WOW' and mouseClicked:
                moveOperation(userName,boxx,boxy)
                drawBoard(board)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def exitWorld(userName):
    """退出游戏世界
    :returns: @todo

    """
    s.settimeout(1)
    userNameTemp = userName
    userLocation = (9999, 9999)
    formatStr = '!'+'3s1i1i'  # 打包 格式化字符串
    #formatStr = "!3s4s4s"
    sendPacked = struct.pack(formatStr, str(userNameTemp),userLocation[0], userLocation[1])
    s.sendto(sendPacked, serverAddr)
    #receivedData = s.recv(2048)
    #formatStrUnpack = '!'+('3s1i1i'*usersNum)  # 打包 格式化字符串
    #receivedDataUnpacked = struct.unpack(formatStrUnpack, receivedData)
    #receivedDataUnpacked =list(receivedDataUnpacked)
    #board = CreatNewWorld(receivedDataUnpacked)
    #return board
def refreshWorld():
    """@todo: Docstring for refreshWorld.
    :arg1: @todo
    :returns: @todo
    """
    s.settimeout(1)
    userNameTemp = 'xxx'
    userLocation = (0, 0)
    formatStr = '!'+'3s1i1i'  # 打包 格式化字符串
    #formatStr = "!3s4s4s"
    sendPacked = struct.pack(formatStr, str(userNameTemp),userLocation[0], userLocation[1])
    s.sendto(sendPacked, serverAddr)
    receivedData = s.recv(2048)
    formatStrUnpack = '!'+('3s1i1i'*usersNum)  # 打包 格式化字符串
    receivedDataUnpacked = struct.unpack(formatStrUnpack, receivedData)
    receivedDataUnpacked =list(receivedDataUnpacked)
    board = CreatNewWorld(receivedDataUnpacked)
    return board


def moveOperation(userName, boxx, boxy):
    """发送移动包，收到包，刷新世界
    :returns: @todo
    """
    s.settimeout(1)
    userNameTemp = userName
    userLocation = (boxx, boxy)
    formatStr = '!'+'3s1i1i'  # 打包 格式化字符串
    #formatStr = "!3s4s4s"
    sendPacked = struct.pack(formatStr, str(userNameTemp),userLocation[0], userLocation[1])
    s.sendto(sendPacked, serverAddr)
    receivedData = s.recv(2048)
    formatStrUnpack = '!'+('3s1i1i'*usersNum)  # 打包 格式化字符串
    receivedDataUnpacked = struct.unpack(formatStrUnpack, receivedData)
    receivedDataUnpacked =list(receivedDataUnpacked)
    board = CreatNewWorld(receivedDataUnpacked)
    return board
def getRandomizedBoard(): # V1.1
    """
    初始化世界
    """
    # Create the board data structure, with randomly placed icons.
    global board
    #i=0
    board = []
    userAndLocation = [['WOW'], [0, 0]]
    #userAndLocation = [[i], [i+1, i+2]]
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            #column.append(userAndLocation)
            #column.append(copy._deepcopy_list(userAndLocation))
            column.append(copy.deepcopy(userAndLocation))
        board.append(column)
    return board
def CreatNewWorld(bufunPacked):
    global board
    """
    更新世界数据
    bufunPacked 是unpack得到的数据，并且已先调用了list()从元组转成了 list """
    for width in range(BOARDWIDTH):
        for height in range(BOARDHEIGHT):
            board[width][height][0][0] = bufunPacked[0]
            del bufunPacked[0]
            board[width][height][1][0] = bufunPacked[0]
            del bufunPacked[0]
            board[width][height][1][1] = bufunPacked[0]
            del bufunPacked[0]
    return board

def initUserLocation(justLogin,revealedBoxes):
    if justLogin:
        revealedBoxes[0][0] = True
    else:
        revealedBoxes[0][0] = False

def enterWorld(userNameTemp):
    global closeLoginWindow,userName,board
    s.settimeout(1)
    userLocation = (0, 0)
    formatStr = '!'+'3s1i1i'  # 打包 格式化字符串
    #formatStr = "!3s4s4s"
    sendPacked = struct.pack(formatStr, str(userNameTemp),userLocation[0], userLocation[1])
    s.sendto(sendPacked, serverAddr)
    receivedData = s.recv(2048)
    formatStrUnpack = '!'+('3s1i1i'*usersNum)  # 打包 格式化字符串
    receivedDataUnpacked = struct.unpack(formatStrUnpack, receivedData)
    receivedDataUnpacked =list(receivedDataUnpacked)
    board = CreatNewWorld(receivedDataUnpacked)
    if receivedData:
        closeLoginWindow = 1
    return board,closeLoginWindow


def showWellcomUser(userName):
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    userName = 'Wellcom ' + userName
    showWellcomUserSurfaceObj = fontObj.render(userName, True, GREEN, NAVYBLUE)
    #wellcomRectObj = wellcomSurfaceObj.get_rect()
    #wellcomRectObj.center = (200, 150)
    DISPLAYSURF.blit(showWellcomUserSurfaceObj, (15,20))
    #pygame.display.update()
def showEnterHint():
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    wellcomSurfaceObj = fontObj.render('Enter Your UserName (Submit with "ENTER" key)', True, GREEN, NAVYBLUE)
    #wellcomRectObj = wellcomSurfaceObj.get_rect()
    #wellcomRectObj.center = (200, 150)
    DISPLAYSURF.blit(wellcomSurfaceObj, (55,150))
    #pygame.display.update()

def EnterUserName(event):
    global userName
    userName += event.unicode
    fontObj = pygame.font.Font('freesansbold.ttf', 22)
    userNameSurfaceObj = fontObj.render(userName, True, ORANGE, NAVYBLUE)
    #userNameRectObj = userNameSurfaceObj.get_rect()
    #userNameRectObj.center = (10, 20)
    DISPLAYSURF.blit(userNameSurfaceObj, (255,200))
    #pygame.display.update()
def drawGirl(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    DISPLAYSURF.blit(catImg, (left,top))
    #revealedBoxes = generateRevealedBoxesData(False)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    #pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)
    DISPLAYSURF.blit(catImg, (left,top))

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)



def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


#def drawBoard():
    ## Draws all of the boxes at the beginning of game.
    #for boxx in range(BOARDWIDTH):
        #for boxy in range(BOARDHEIGHT):
            #left, top = leftTopCoordsOfBox(boxx, boxy)
            #pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

def drawBoard(board):
    global revealedBoxes
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if board[boxx][boxy][0][0] != 'WOW':
                #revealedBoxes[boxx][boxy] = True
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
                drawGirl(boxx, boxy)
            else:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            #if not revealed[boxx][boxy]:
                ## Draw a covered box.
                #pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            #else:
                #drawGirl(boxx, boxy)
#def getRandomizedBoard():
    ## Get a list of every possible shape in every possible color.
    #icons = []
    #for color in ALLCOLORS:
        #for shape in ALLSHAPES:
            #icons.append( (shape, color) )

    #random.shuffle(icons) # randomize the order of the icons list
    #numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    #icons = icons[:numIconsUsed] * 2 # make two of each
    #random.shuffle(icons)

    ## Create the board data structure, with randomly placed icons.
    #board = []
    #for x in range(BOARDWIDTH):
        #column = []
        #for y in range(BOARDHEIGHT):
            #column.append(icons[0])
            #del icons[0] # remove the icons as we assign them
        #board.append(column)
    #return board


def generateRevealedBoxesData(val):
    global revealedBoxes
    for i in range(BOARDWIDTH):
        listOfHeight = [val]*BOARDHEIGHT
        listdeepcopy= copy.deepcopy(listOfHeight)
        revealedBoxes.append(listdeepcopy)
        #revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes



if __name__ == '__main__':
    main()


