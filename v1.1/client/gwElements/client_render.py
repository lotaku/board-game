#!/usr/bin/env python
# encoding: utf-8
import pygame
class ClientRender():
    def __init__(self):
        self.fps=30
        self.fpsClock= pygame.time.Clock()

    def render(self):
        pygame.display.update()
        self.fpsClock.tick(self.fps)

clientRender=ClientRender()
