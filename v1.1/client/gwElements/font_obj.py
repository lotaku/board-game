#!/usr/bin/env python
# encoding: utf-8
import pygame
class FontObj():
    """返回 text 对应的 self.textSurf 对象"""
    def __init__(self,text):
        self.fontSize = 22
        self.font = "freesansbold.ttf"
        self.text=text
        self.color = (255,   0,   0) #RED
        self.bgcolor = ( 60,  60, 100)#NAVYBLUE
        self.top=0
        self.left=0
        self.topleft=(0,0)
        self.makeFontObj()

        #self.makeText()
    def makeFontObj(self):
        pygame.init()
        fontObj = pygame.font.Font(self.font,self.fontSize)
        self.textSurf = fontObj.render(self.text,True,self.color,self.bgcolor)
        self.textRect = self.textSurf.get_rect()
        self.textRect.topleft=self.topleft

    def changeTopleft(self,top,left):
        """self.textRect = top,left"""
        self.topleft =(top,left)
        self.textRect.topleft=self.topleft

    def changeColor(self,color,bgcolor):
        self.color = color
        self.bgcolor = bgcolor
        self.makeFontObj()
