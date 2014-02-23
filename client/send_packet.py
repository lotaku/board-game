#!/usr/bin/env python
# encoding: utf-8
import tcp_client

class SendPacket:
    def __init__(self,id):
        self.buffer=chr(id)
    def packInt(self,value):
        self.buffer+=chr(value/0x100)+chr(value%0x100)

    def packString(self,text):
        self.packInt(len(text))
        self.buffer+=text

    def send(self):
        length=len(self.buffer)
        buffer=chr(length/0x100)+chr(length%0x100)+self.buffer
        tcp_client.tcpClient.sendData+=buffer
        print '这个是请求进入世界的buffer：',tcp_client.tcpClient.sendData




