#!/usr/bin/env python
# encoding: utf-8
from tcp_client import tcpClient
import gwdata
#from player import player
#import pygame
#import class_manager
class Client:

    def __init__(self):
        #tcpClient.connect()
        gwdata.gameWorld.play()
        #gwdata.hint_enterYourName.blit()
        gwdata.loginWin.loop()
        #gwdata.initGameWorld()

    def loop(self):
        while True:
            #tcpClient.recvPackets()
            #tcpClient.handlePackets()
            #self.handleEvents()
            self.render()
            #tcpClient.sendPackets()
            #gwdata.freshLOCAL_PLAYER()
            #gwdata.exitGame()

    def handleEvents(self):
        gwdata.playermove()
    def render(self):
        gwdata.clientRender.render()

client=Client()
client.loop()

