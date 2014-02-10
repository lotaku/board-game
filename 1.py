import random,pygame,sys
from pygame import *


#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF=pygame.display.set_mode((300, 400))
pygame.display.set_caption('11')
DISPLAYSURF.fill(YELLOW)

pygame.display.update()
FPSCLOCK.tick(30)
