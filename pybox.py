# pybox.py - Sandbox for pygame testing
# nitor
# Jun 2014

import pygame, sys
from pygame.locals import *


res = (640, 480) # resolution

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfObj = pygame.display.set_mode(res)
pygame.display.set_caption('pybox')

red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)

mousex, mousey = 0, 0

fontObj = pygame.font.Font('freesansbold.ttf', 32)
msg = 'Hello pygame!'

coords1 = (60, 160)
coords2 = (120, 60)
thick = 4

# main program loop
while True:

    # draw
    windowSurfObj.fill(white)
    
    pygame.draw.line(windowSurfObj, blue, (mousex, mousey), coords2, thick)
    

    # process input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            if event.button == 1:
                pass
            elif event.button == 2:
                pass
            elif event.button == 3:
                pass
                
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
        
    else:
        pass

    # update draw
    pygame.display.update()
    fpsClock.tick(30)
