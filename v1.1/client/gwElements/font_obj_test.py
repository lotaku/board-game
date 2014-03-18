#!/usr/bin/env python
# encoding: utf-8
import unittest
import pygame
from font_obj import FontObj

class Test_FontObj(unittest.TestCase):
    def test_init(self):
        self.text = "Game Start"
        newFontObj = FontObj(self.text)
        self.assertIs (pygame.Rect,type(newFontObj.textRect))
        self.assertIs (pygame.Surface,type(newFontObj.textSurf))

if __name__ == "__main__":
    unittest.main()
