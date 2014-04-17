#!/usr/bin/env python
# encoding: utf-8

class MenuClick():
    """
    鼠标点击在菜单上
    """
    def __init__(self):
        pass

    def clickOnMenu(self,menuArgm,mousex,mousey):
        for key ,rect in menuArgm.menuOptionRects.items():
            if rect.collidepoint(mousex,mousey):
                if key==0:
                    menuArgm.menuOption[key][1]()
                else:
                    menuArgm.menuOption[key][1](menuArgm.ofPlayer)
                menuArgm.isNotShowing=1

menuClick=MenuClick()
