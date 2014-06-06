# pybox.py - Sandbox for pygame testing
# nitor
# Jun 2014

import pygame, sys
from pygame.locals import *


res = (1366, 768) # resolution

coords1 = (60, 160)
coords2 = (120, 60)
thick = 4

scrollSpeed = 3

mousex, mousey = 0, 0


# setup

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfObj = pygame.display.set_mode(res)
pygame.display.set_caption('pybox')

red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)

fontObj = pygame.font.Font('freesansbold.ttf', 16)
msg = 'Hello pygame!'



def processInput():
    global coords1, coords2, msg, mousex, mousey
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            if event.button == 1:
                msg = 'left click'
            elif event.button == 2:
                msg = 'middle click'
            elif event.button == 3:
                msg = 'right click'
            elif event.button == 4:
                msg = 'scroll up'
                coords2 = (coords2[0], coords2[1] - scrollSpeed)
            elif event.button == 5:
                msg = 'scroll down'
                coords2 = (coords2[0], coords2[1] + scrollSpeed)
                
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))


# main program loop
while True:

    # draw
    windowSurfObj.fill(white)
    
    pygame.draw.line(windowSurfObj, blue, (mousex, mousey), coords2, thick)
    
    msgSurfObj = fontObj.render(msg, False, black)
    msgRectObj = msgSurfObj.get_rect()
    msgRectObj.topleft = (res[0]/4,20)
    windowSurfObj.blit(msgSurfObj, msgRectObj)

    
        
    processInput()

    # update draw
    pygame.display.update()
    fpsClock.tick(30)

    

    
def draw ():
    pass
