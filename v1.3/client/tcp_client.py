#!/usr/bin/env python
# encoding: utf-8

from select import select
from socket import socket
from socket import AF_INET, SOCK_STREAM
from packet import CRecvPacket
#from packet import CSendPacket
from opccode import GS2CHandlerChoice

class CTcpClient:

    def __init__(self):
        self.m_ConnectSocket=socket(AF_INET, SOCK_STREAM)
        self.m_SendData = ''
        self.m_RecvData = ''
        self.m_Buffers = []

        self.m_Host = 'localhost'
        self.m_Port = 8888

    def Connect(self):
        self.m_ConnectSocket.connect((self.m_Host,self.m_Port))
        self.m_ConnectSocket.setblocking(0)

    def RecvPackets(self):
        reads, _, errors =select([self.m_ConnectSocket], [], [],0.0001)
        if self.m_ConnectSocket in reads:
            self.Read()

    def SendPackets(self):
        _, writes, errors = select([], [self.m_ConnectSocket], [], 0.0001)
        if self.m_ConnectSocket in writes:
            self.Write()

    def HandlePackets(self):
        for buffer in self.m_Buffers:
            packet=CRecvPacket(buffer)
            GS2CHandlerChoice(packet)

    def Read(self):
        data = self.m_RecvData +self.m_ConnectSocket.recv(1024)
        if data:
            dataLength = len(data)
            lengthBeginIndex = 0
            contentBeginIndex = 2

            if dataLength >= contentBeginIndex:
                contentLength = ord(data[lengthBeginIndex])*0x100 + ord(data[lengthBeginIndex+1])
                packetLength = contentBeginIndex + contentLength
                while dataLength >= packetLength:
                    content = data[contentBeginIndex:contentBeginIndex+contentLength]
                    self.m_Buffers.append(content)
                    data=data[contentBeginIndex+contentLength:]
                    dataLength = len(data)
                    if dataLength >= contentBeginIndex:
                        contentLength = ord(data[lengthBeginIndex])*0x100 + ord(data[lengthBeginIndex+1])
                        packetLength = contentBeginIndex + contentLength
                    else:
                        break
                self.m_RecvData = data
        else:
            pass

    def Write(self):
        data = self.m_SendData
        if len(data):
            amount = self.m_ConnectSocket.send(data)
            self.m_SendData = data[amount:]






