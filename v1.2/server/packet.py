#!/usr/bin/env python
# encoding: utf-8
class RecvPacket:

    def __init__(self,buffer):
        self.id=ord(buffer[0])
        self.buffer=buffer
        self.currentIndex=1

    def unpackInt(self):
        index = self.currentIndex
        value=ord(self.buffer[index])*0x100+ord(self.buffer[index+1])
        self.currentIndex+=2
        return value
    def unpackString(self):
        length=self.unpackInt()
        string=self.buffer[self.currentIndex:self.currentIndex+length]
        self.currentIndex+=length
        return string
class SendPacket:

    def __init__(self,id):
        self.buffer =chr(id)

    def packInt(self,value):
        self.buffer+=chr(value/0x100)+chr(value%0x100)

    def packString(self,text):
        self.packInt(len(text))
        self.buffer+=text

    def send(self,player):
        length =len(self.buffer)
        buffer=chr(length/0x100)+chr(length%0x100)+self.buffer
        player.sendData+=buffer

    def sendOther(self,player):
        length =len(self.buffer)
        buffer=chr(length/0x100)+chr(length%0x100)+self.buffer
        player.broadBuff+=buffer


