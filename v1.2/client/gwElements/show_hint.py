#!/usr/bin/env python
# encoding: utf-8
from font_obj import FontObj
from game_win import gameWin

class ShowHint():
    def __init__(self):
        self.color = (  0, 255,   0)#GREEN
        self.bgcolor =( 60,  60, 100)#NAVYBLUE
        self.fontSize = 22
        self.font = "freesansbold.ttf"
    def updateText(self,text,coordinates):
        self.text = text
        self.coordinates = coordinates
        fontObj = FontObj(self.text)
        self.textSurf= fontObj.textSurf
    def blit(self):
        gameWin.displaySurf.blit(self.textSurf, self.coordinates)
