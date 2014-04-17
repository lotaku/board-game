#!/usr/bin/env python
# encoding: utf-8
from game_win import gameWin
class Blit():
    def __init__(self):
        pass
    def blitFont(slef,fontObj):
        gameWin.displaySurf.blit(fontObj.textSurf,fontObj.textRect)

blit=Blit()
