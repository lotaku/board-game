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
        #以后此类对象surf,rect的属性，尽力定义为 self.surt,self.rect 方便记忆和调用
        #在invitation 类中调用到
        self.rect = self.textRect
        self.surf = self.textSurf

    def changeTopleft(self,top,left):
        """self.textRect = top,left"""
        self.topleft =(top,left)
        self.textRect.topleft=self.topleft

    def changeColor(self,color,bgcolor):
        self.color = color
        self.bgcolor = bgcolor
        self.makeFontObj()
