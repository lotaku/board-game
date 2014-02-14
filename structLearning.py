#!/usr/bin/env python
# encoding: utf-8
import random
import pprint
import struct
import copy
WINDOWWIDTH = 680
WINDOWHEIGHT=580
BOXSIZE=85
GAPSIZE=10
BOARDWIDTH = 2
BOARDHEIGHT = 2
usersNum = BOARDWIDTH * BOARDHEIGHT  # 计算可容纳的用户总数
# test1
#floatlist = [random.random() for _ in range(10*5)]
#floatlist = [_ for _ in range(10*5)]
#buf = struct.pack('%sf' % len(floatlist), *floatlist)
#buf2 = struct.unpack('50f' ,buf)
##print len(floatlist)
#print len(buf)
#print buf2

# -------------test 2 -------------------

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
#pprint.pprint ( getRandomizedBoard() )

board = getRandomizedBoard()
# 成功单个赋值  搜索谷歌想起 list的 shallow copies 特性，以及想起用 deepcopy()
#board[0][0][1][0]= 4
#board[0][0][1][1]= 5
#pprint.pprint(board) # 看到4个[ ，四重循环。解析 用： #list2 = [z for i in board for j in i for k in j for z in k]
#board[0][0][0][0]='jan'
#pprint.pprint(board)
# 初始化 2个 盒子，即 2个人物
#board[0][0][0][0]= 'Jan'
#board[0][0][1][0]= '1'
#board[0][0][1][1]= '2'

#board[0][1][0][0]= 'Ton'
#board[0][1][1][0]= '1'
#board[0][1][1][1]= '2'
print '初始化的世界'
pprint.pprint(board)
# 以上代码块 --- 成功单个赋值  搜索谷歌想起 list的 shallow copies 特性，以及想起用 deepcopy()

def getEveryEle():
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

arrBoard = getEveryEle() #成功获得一维数组
print '成功获得一维数组'
pprint.pprint(arrBoard)

# 打包 解包
print '元素个数：', len (arrBoard)
formatStr = '!'+('3s1i1i'*usersNum)  # 打包 格式化字符串
buf = struct.pack(formatStr, *arrBoard )
print '打包后的数据'
print buf
bufunPacked = struct.unpack(formatStr, buf)
print '解包后的数据'
print repr(bufunPacked)
bufunPacked = list(bufunPacked)
print '转化成列表'
print bufunPacked
CreatNewWorld(bufunPacked)
print '创建新的世界'
pprint.pprint(board)
# test 1 成功
#list2 = [i4 for i1 in board for i2 in i1 for i3 in i2 for i4 in i3]
#len1=len(list2)
#print len(list2)
#pprint.pprint(list2)
# test 1 END

# test 2
#list3 = [[False,False]]
#list3[0][0] = 1
#pprint.pprint(list3[0][0])
# test 2 END
# 以下代码块 自动 递归 解析 多维数组 获取元素，先谷歌
#def getAllele(forNum,board): # 再这里，计算盒子数   forNum =  宽x高
    #listStr = ''
    #maxNum = forNum
    #for i in range(forNum):
        #lisStr += 'i%d for '

# 以上代码块------- 自动 递归 解析 多维数组 获取元素，先谷歌

