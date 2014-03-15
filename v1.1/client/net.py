#!/usr/bin/env python
# encoding: utf-8
import socket

def recvPackets():
    pass

def sendPackets():
    pass

class RecvPacket:

    def __init__(self,buff):
        self.buff=buff
        self.currentIndex=0

    def unpackInt(self,size):
        return int

    def unpackStr(self):
        return str

class SendPacket:

    def __init__(self):
        self.buffer=""

    def packInt(self,value,size):
        "压入一个size字节的整数value"

    def packString(self,text):
        "压入字符串text,先压一个正数代表长度，然后压内容"
        self.addInt(len(text),size)
        #todo

    def send(self):
        send(self.buff) #todo

def GS2CEnterWorld(packet):
    "更新客户端数据"

def GS2CPlayerMove(packet):
    "更新客户端数据"

def C2GSEnterWorld():
    packet=Packet(1) #包的协议号
    packet.addString(name) #玩家名字
    packet.send()

def C2GSEnterWorld():
    packet=Packet(2) #包的协议号
    packet.addInt(x,1) #一个字节的正数代表x坐标
    packet.addInt(y,1) #
    packet.send()

#网络包理函数字典
handle={
    1:GS2CEnterWorld,
    2:GS2CPlayerMove,
}

#注意客户端面对的模型 一个自己对服务器
#服务器的模型是 一个服务器对多个客户端
def connectServer():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #clientSocket.setblocking(0)
    serverAddress = ("", 51423)
    clientSocket.connect(serverAddress)
    sendPacket =SendPacket("User1 0 0")
    sendPacket.


def handlePackets():
    packets=recvPackets()
    for packet in packet:
        packetId=packet.id
        handle[packetsId](packet)


