#!/usr/bin/env python
# encoding: utf-8
from gwElements.tcp_client import tcpClient
#import gwElements.gwdata as gwdata
import gwdata
class Client:

    def __init__(self):
        tcpClient.connect()
        gwdata.gameWin.play()
        gwdata.loginWin.loop()
        gwdata.gameWorld.createMap()

    def loop(self):
        while True:
            tcpClient.recvPackets()
            tcpClient.handlePackets()
            self.handleEvents()
            self.render()
            tcpClient.sendPackets()

    def handleEvents(self):
        gwdata.playerAction.mouseCapture()
    def render(self):
        gwdata.clientRender.render()

if '__main__' == __name__ :
    client=Client()
    client.loop()

