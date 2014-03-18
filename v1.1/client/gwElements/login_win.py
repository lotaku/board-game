#!/usr/bin/env python
# encoding: utf-8
import sys
import pygame
from player import localPlayer
from show_hint import ShowHint
from pygame.locals import K_ESCAPE,QUIT,KEYUP,K_RETURN
from client_render import clientRender
from font_obj import FontObj
from game_win import gameWin
class LoginWin():
    def __init__(self):
        pass

    def loop(self):
        self.hint_enterYourName = ShowHint()
        self.hint_enterYourName.updateText('Enter Your UserName (Submit with "ENTER" key)',(50,80))
        self.hint_enterYourName.blit()
        while True:
            breakKey=0
            for event in pygame.event.get():
                if event.type == QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key != K_RETURN:
                    self.enterPlayerName(localPlayer,event)
                elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                    print "commit something..."
                    localPlayer.c2gsEnterWorld()
                    breakKey=1
            if breakKey:
                break
            clientRender.render()

    def enterPlayerName(self,playerArgm,event):
        playerArgm.name += event.unicode
        localPlayerNameText = FontObj(playerArgm.name)
        gameWin.displaySurf.blit(localPlayerNameText.textSurf,(255,200))


loginWin=LoginWin()
