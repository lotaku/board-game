#!/usr/bin/env python
# encoding: utf-8
import pygame
from pygame.locals import K_ESCAPE,QUIT,KEYUP,MOUSEBUTTONDOWN
from player import localPlayer
from game_world import gameWorld
from player_manager import playerManager
from draw_ import draw
from menu import rightMenu

class PlayerAction():
    def __init__(self):
        pass

    def moveCapture(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                localPlayer.c2gsExitGame()
            elif event.type == MOUSEBUTTONDOWN :
                mousex,mousey = event.pos

                if event.button == 1:
                    mousex,mousey = event.pos
                    boxx,boxy = gameWorld.getBoxAtPixel(mousex,mousey)
                    if boxx !=None and boxy != None:
                        localPlayer.c2gsPlayerMove(boxx,boxy)
                if event.button == 3:  # 鼠标右击,判断是否画出右键菜单
                    mousex,mousey = event.pos
                    boxx,boxy = gameWorld.getBoxAtPixel(mousex,mousey)
                    if boxx != None and boxy != None:
                        #判断x,y 是否有玩家,并取得该玩家
                        for _,playerUnderMouse in playerManager.players.items():
                            if playerUnderMouse.x == boxx and playerUnderMouse.y == boxy:
                                #playerUnderMouseArgm = playerUnderMouse
                                draw.drawMenu(rightMenu,boxx,boxy)
playerAction= PlayerAction()
