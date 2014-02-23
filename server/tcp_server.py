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
        player.sendData = ''
        playerManager.add(player)
        self.remoteSockets.append(remote)

    def readRemoteData(self,readSocket):
        print "正在readRemoteData"
        data=self.remoteData.get(readSocket,'')+readSocket.recv(1024)
        if data:
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
        print "正在writeRemot"
        player = playerManager.get(writeSocket)
        data = player.sendData
        amount=writeSocket.send(data)
        player.sendData=data[amount:]
        if not len(player.sendData):
            self.writeRemoteSockets.remove(writeSocket)









