#!/usr/bin/env python
# encoding: utf-8

from select import select
from socket import socket
from socket import AF_INET,SOCK_STREAM
from socket import SOL_SOCKET,SO_REUSEADDR
from packet import RecvPacket

from opccode import handlePacket
from player import Player
from player_manager import playerManager

class TcpServer:

    def __init__(self):
        self.listenSocket=socket(AF_INET,SOCK_STREAM)
        self.listenSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.listenSocket.setblocking(0)

        self.remoteSockets=[]
        self.writeRemoteSockets=[]
        self.remoteData={}
        self.buffers={}

    def listen(self,host='localhost',port=8888):
        self.listenSocket.bind((host,port))
        self.listenSocket.listen(11)

    def run(self):
        while True:
            #reads,writes,errors=select([self.listenSocket]+self.remoteSockets, self.remoteSockets,[],0.0001)
            reads,writes,errors=select([self.listenSocket]+self.remoteSockets, self.writeRemoteSockets,[],0.0001)

            for read in reads:
                if read is self.listenSocket:
                    self.acceptConnection()
                else:
                    self.readRemoteData(read)
                    print ' 正在read'
                    self.handlePackets()
            for write in writes:
                self.writeRemote(write)

            # 通知其他客户端
            for write in writes:
                self.writeOtherRemote(write)


    def handlePackets(self):
        print ' 正在handlePackets'
        for remote,buffers in self.buffers.items():
            player=playerManager.get(remote)
            for buffer in buffers:
                packet = RecvPacket(buffer)
                handlePacket(player,packet)
        self.buffers={}


    def acceptConnection(self):
        print "正在acceptConnection"
        remote,address=self.listenSocket.accept()
        remote.setblocking(0)
        player=Player(remote)
        #player.sendData = ''
        #player.broadBuff=""
        playerManager.add(player)
        self.remoteSockets.append(remote)

    def readRemoteData(self,readSocket):
        print "正在readRemoteData"
        data=self.remoteData.get(readSocket,'')+readSocket.recv(1024)
        if data:
            if readSocket not in self.writeRemoteSockets:
                self.writeRemoteSockets.append(readSocket)
            dataLength=len(data)
            print "recv"
            for char in data:
                print "\t",ord(char)

            lengthBeginIndex  = 0
            contentBeginIndex = 2

            if dataLength>contentBeginIndex:
                contentLength=ord(data[lengthBeginIndex])*0x100+ord(data[lengthBeginIndex+1])
                packetLength=contentBeginIndex+contentLength
                while dataLength >= packetLength:
                    content=data[contentBeginIndex:contentBeginIndex+contentLength]
                    self.buffers.setdefault(readSocket,[]).append(content)
                    data=data[contentBeginIndex+contentLength:]
                    dataLength=len(data)
                    if dataLength>contentBeginIndex:
                        contentLength=ord(data[lengthBeginIndex])*0x100+ord(data[lengthBeginIndex+1])
                        packetLength=contentBeginIndex+contentLength
                    else:
                        break
            self.remoteData[readSocket]=data
            print self.buffers
        else:
            self.remoteSockets.remove(readSocket)

    def writeRemote(self,writeSocket):
        #=== 兼顾多客户端====
        removeKey = 1
        print "正在writeRemot"
        for playerSocket,player in playerManager.socketPlayer.items():
            data = player.sendData
            amount=playerSocket.send(data)
            player.sendData=data[amount:]
            if len(player.sendData):
                removeKey = 0 # 还不能把 writeSocket 从 select write 移除
        if removeKey ==1 :
            try:
                self.writeRemoteSockets.remove(writeSocket)
            except:
                pass
        #=====单客户端代码====
        #print "正在writeRemot"
        #player = playerManager.get(writeSocket)
        #data = player.sendData
        #amount=writeSocket.send(data)
        #player.sendData=data[amount:]
        ##if not len(player.sendData) and True:
        #if not len(player.sendData) and not len(player.broadBuff):# 为“广播”添加一个条件
            #try:
                #self.writeRemoteSockets.remove(writeSocket)
            #except:
                #pass

    def writeOtherRemote(self,writeSocket):
            #======多客户端广播代码,多加一个player.buff，prim 说不用，都挂在不同player的sendData后面就行====
            print "正在writeRemot"

            player = playerManager.get(writeSocket)
            data = player.broadBuff

            for OtherSocket, _ in playerManager.socketPlayer.items():
                if len(playerManager.socketPlayer)<=1:
                    player.broadBuff=''
                else:
                    if OtherSocket != writeSocket:
                        amount=OtherSocket.send(data)
                        player.broadBuff=data[amount:]

            if not len(player.sendData) and not len(player.broadBuff):
                try:
                    self.writeRemoteSockets.remove(writeSocket,'')
                except:
                    pass
            if player.exitKey:
                #用户退出游戏
                #从服务器消除该用户的信息
                #del playerManager.socketPlayer[player.socket]
                playerManager.remove(player)
                #移除该用户的socket
                try:
                    #self.writeRemoteSockets.remove(writeSocket,'')
                    self.writeRemoteSockets.remove(writeSocket)
                except:
                    pass






