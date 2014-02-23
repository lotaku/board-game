#!/usr/bin/env python
# encoding: utf-8
from tcp_client import tcpClient
import sys
import gwdata
#import player
from player import player
import pygame
class Client:

    def __init__(self):
        tcpClient.connect()
        gwdata.loginWin()
        gwdata.initGameWorld()
        #player.create('fzz')
        #player.c2gsEnterWorld()


    def loop(self):
        while True:
            tcpClient.recvPackets()
            tcpClient.handlePackets()
            self.handleEvents()
            self.render()
            tcpClient.sendPackets()



    def handleEvents(self):
        gwdata.playermove()
    def render(self):
        gwdata.clientRender()
        #pygame.display.update()
        #gwdata.FPSCLOCK.tick(30)


client=Client()
client.loop()

