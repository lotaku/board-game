#!/usr/bin/env python
# encoding: utf-8
from tcp_client import tcpClient
import gwdata
#from player import player
#import pygame
#import class_manager
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
            #gwdata.freshLOCAL_PLAYER()
            gwdata.exitGame()

    def handleEvents(self):
        gwdata.playerAction.moveCapture()
    def render(self):
        gwdata.clientRender.render()

if '__main__' == __name__ :
    client=Client()
    client.loop()

