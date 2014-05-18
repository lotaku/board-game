#!/usr/bin/env python
# encoding: utf-8
#temp add path
#import sys, os
#if os.path.abspath('..') not in sys.path:
    #sys.path.append(os.path.abspath('..'))
    #print os.path.abspath('..')

from select import select
from socket import socket
from socket import AF_INET, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR
from player import CPlayer
from player import playerManager
from packet import CRecvPacket
#from packet import CSendPacket
from network import C2GSTcpHandler




class CTcpServer:

    def __init__(self):
        self.m_ListenSocket=socket(AF_INET, SOCK_STREAM)
        self.m_ListenSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.m_ListenSocket.setblocking(0)

        self.m_Host='localhost'
        self.m_Port=8888

        self.m_RemoteSockets=[]
        self.m_RemoteData={}

        self.m_WriteRemoteSockets=[]
        self.m_Buffers={}

    def Listen(self):
        self.m_ListenSocket.bind((self.m_Host, self.m_Port))
        self.m_ListenSocket.listen(11)

    def AcceptConnection(self):
        remoteSocket,address = self.m_ListenSocket.accept()
        remoteSocket.setblocking(0)

        self.m_RemoteSockets.append(remoteSocket)



    def ReadRemoteData(self, readSocket):
        try:
            data=self.m_RemoteData.get(readSocket, '')+readSocket.recv(1024)
        except:
            data=self.m_RemoteData.get(readSocket, '')
        if data:
            if readSocket not in self.m_WriteRemoteSockets:
                self.m_WriteRemoteSockets.append(readSocket)

            dataLength=len(data)
            lengthBeginIndex = 0
            contentBeginIndex = 2

            if dataLength>contentBeginIndex:
                contentLength = ord(data[lengthBeginIndex])*0x100 + ord(data[lengthBeginIndex+1])
                packetLength = contentBeginIndex+contentLength

                while dataLength >= packetLength:
                    content = data[contentBeginIndex:contentBeginIndex+contentLength]
                    self.m_Buffers.setdefault(readSocket,[]).append(content)
                    data = data[contentBeginIndex+contentLength:]
                    dataLength = len(data)
                    if dataLength>contentBeginIndex:
                        contentLength = ord(data[lengthBeginIndex])*0x100 + ord(data[lengthBeginIndex+1])
                        packetLength = contentBeginIndex+contentLength
                    else:
                        break
            else:
                self.m_RemoteData[readSocket] = data


    def HandlePackets(self):
        for remoteSocket, buffers in self.m_Buffers.items():
            for buffer in buffers:
                packet = CRecvPacket(buffer)
                C2GSTcpHandler[packet.m_HandlerClassId](remoteSocket, packet)

    #其他帮助函数
    def SetHostAndPort(self, host, port):
        self.m_Host = host
        self.m_Port = port

    def Run(self):
        while True:
            reads, writes, errors = select([self.m_ListenSocket]+self.m_RemoteSockets, self.m_WriteRemoteSockets, [], 0.0001)

            for read in reads:
                if read is self.m_ListenSocket:
                    self.AcceptConnection()
                else:
                    self.ReadRemoteData(read)
                    self.HandlePackets()



