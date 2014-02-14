#!/usr/bin/env python
# encoding: utf-8

from SocketServer import UDPServer, \
        DatagramRequestHandler, \
        ForkingMixIn, \
        BaseRequestHandler #, ForkingUDPServer
import struct

import random
import pprint
import copy

board = []
WINDOWWIDTH = 680
WINDOWHEIGHT=580
BOXSIZE=85
GAPSIZE=10
BOARDWIDTH = 2
BOARDHEIGHT = 2
usersNum = BOARDWIDTH * BOARDHEIGHT  # 计算可容纳的用户总数

def getEveryEle(board):
    """
     获得初始世界的每一个元素 组成新的一维数组，用于socket pack 传递
    """
    arrBoard = []
    for width in range(BOARDWIDTH):
        for height in range(BOARDHEIGHT):
            userName = board[width][height][0][0]
            boxx = board[width][height][1][0]
            boxy = board[width][height][1][1]
            arrBoard.append(userName)
            arrBoard.append(boxx)
            arrBoard.append(boxy)
    return arrBoard

def CreatNewWorld(bufunPacked):
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

#def getRandomizedBoard():# V1.0 单机时，初始化世界
    ## Create the board data structure, with randomly placed icons.
    #global board
    #board = []
    #userAndLocation = [False, [False, False]]
    #for x in range(BOARDWIDTH):
        #column = []
        #for y in range(BOARDHEIGHT):
            #column.append(userAndLocation)
        #board.append(column)
    #return board


def getRandomizedBoard(): # V1.1
    """
    初始化世界
    """
    # Create the board data structure, with randomly placed icons.
    global board
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
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


#class boardGameRequestHandler(BaseRequestHandler):
class boardGameRequestHandler(BaseRequestHandler):
    def handle(self):
        global board
        receivedData = self.request[0]#.strip()
        socket = self.request[1]
        formatStr = '!'+'3s1i1i'  # 打包 格式化字符串
        #formatStr = "!3s4s4s"
        unpackedreceivedData = struct.unpack(formatStr,receivedData)
        #print "{} wrote:".format(self.client_address[0])
        #print "{} wrote:".format(self.client_address[1])
        #print "Wellcome {}.".format(unpackedreceivedData)
        #socket.sendto(data.upper(), self.client_address)
        userName = unpackedreceivedData[0]
        boxx = unpackedreceivedData[1]
        boxy = unpackedreceivedData[2]
        board[boxx][boxy][0][0] = userName
        board[boxx][boxy][1][0] = boxx
        board[boxx][boxy][1][1] = boxy
        arrBoard = getEveryEle(board)
        print arrBoard
        formatStrSendto = '!'+('3s1i1i'*usersNum)  # 打包 格式化字符串
        #print struct.calcsize(formatStrSendto)
        worldPacked = struct.pack(formatStrSendto,*arrBoard)
        socket.sendto(worldPacked, self.client_address)

class boardGameServer(UDPServer):
#class boardGameServer(ForkingMixIn, UDPServer):
    allow_reuse_address = 1
if __name__ == "__main__":
    serveraddr = ('', 51423)
    getRandomizedBoard()# Init whole game world date
    #getEveryEle(board)
    #formatStrSendto = '!'+('3s1i1i'*usersNum)  # 打包 格式化字符串
    #print struct.calcsize(formatStrSendto)
    server =  boardGameServer(serveraddr,boardGameRequestHandler)
    server.serve_forever()
