#!/usr/bin/env python
# encoding: utf-8
class RecvPacket:

    def __init__(self,buffer):
        self.id=ord(buffer[0])
        self.buffer=buffer
        self.currentIndex=1

    def unpackInt(self):
        index=self.currentIndex
        value=ord(self.buffer[index])*0x100+ord(self.buffer[index+1])
        self.currentIndex+=2
        return value
    def unpackString(self):
        length=self.unpackInt()
        string=self.buffer[self.currentIndex:self.currentIndex+length]
        self.currentIndex+=length
        return string



