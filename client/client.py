#!/usr/bin/env python
# encoding: utf-8
#client.py
import pygame
import socket
import net
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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
board = []
class Client:

    def __init__(self):
        #global FPSCLOCK, DISPLAYSURF
        ##客户端数据
        #pygame.init
        #FPSCLOCK = pygame.time.Clock()
        #DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.init()

    def init(self):
        net.connectServer()

    def mainLoop(self):
        while True:
            #首先处理服务器发过来的网络，仅更新客户端数据
            net.handlePackets()

            ##处理客户端事件，仅更新客户端数据
            #self.handleEvents()

            ##处理2步可能产生发给服务器的包
            ##这里一起发送
            #net.sendPackets()

            ##更新客户端的这一frame的画面
            #self.render()

client=Client()
#client.mainLoop()
