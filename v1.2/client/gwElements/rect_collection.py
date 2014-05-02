#!/usr/bin/env python
# encoding: utf-8
class RectCollection():
    def __init__(self):
        self.rects={}

    def mouseClick(self,mousex,mousey):
        for obj, funAndArgms in self.rects.items():
            if obj.rect.collidepoint(mousex,mousey):
                #"鼠标左键 点击 在某选项上，开始调用某功能函数..."
                fun = funAndArgms[0]
                argms = funAndArgms[1]
                # N个参数可以放在元组里，通过 *argms 表达式传递,不会以一个元组的 单元传递
                fun(*argms)

rectCollection=RectCollection()

