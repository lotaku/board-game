#!/usr/bin/env python
# encoding: utf-8
import pygame

class GameWin():
    def __init__(self):
        self.WINDOWWIDTH=680
        self.WINDOWHEIGHT=580
        self.caption="Board Game"
        self.bgcolor=(60, 60, 100)
    def play(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.displaySurf=pygame.display.set_mode((self.WINDOWWIDTH,self.WINDOWHEIGHT))
        self.displaySurf.fill(self.bgcolor)

gameWin=GameWin()
