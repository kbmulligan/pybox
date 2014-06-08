# pybox.py - Sandbox for pygame testing
# nitor
# Jun 2014

import pygame, sys, math
from pygame.locals import *

# main program config
debug = False
paused = True
res = (1000, 600) # resolution
borderWidth = 10
bottomPad = 2
fps = 60

# brick layout numbers
brickRows = 3
brickCols = 7
numBricks = brickRows * brickCols
brickPadding = 3
brickVertOffset = 100

# player startup values
startingPoints = 0
startingLives = 5


# color presets
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)

# Class defs
class Player:

    def __init__(self, pts, level):

        self.pts = pts
        self.level = level

    pts = 0
    level = 0
    lives = startingLives

    def getPoints(self):
        return self.pts

    def addPoints(self, newPoints):
        self.pts += newPoints

    def setPoints(self, newPoints):
        self.pts = newPoints

    def takeLife(self):
        self.lives -= 1

    def setLives(self, newLives):
        self.lives = newLives

    def getLives(self):
        return self.lives

    def addLife(self):
        self.lives += 1
    
class Game:

    level = 0

    def __init__(self):
        level = 1

    def setLevel(self, lvl):
        self.level = lvl

    def getLevel(self):
        return self.level
    

        
class Ball:

    x = 50
    y = 50
    
    def __init__ (self, nx, ny):
        self.x = nx
        self.y = ny
    
    size = 10
    mass = 1

    velX = 0
    velY = 0

    def update(self):
        self.x += self.velX
        self.y += self.velY

    def setVelocity(self, newVelX, newVelY):
        self.velX = newVelX
        self.velY = newVelY

    def getPos(self):
        return (int(self.x), int(self.y))

    def setPos(self, nx, ny):
        self.x = nx
        self.y = ny

    def reflect(self, surf):
        if surf == 'horz':
            self.velY *= -1
        elif surf == 'vert':
            self.velX *= -1
        else:
            pass
        

class Paddle:

    def __init__ (self):
        pass
    
    size = 80
    width = 15
    mass = 1
    notch = 5

    x = res[0]/2 - size/2
    y = res[1] - 70

    velX = 5
    velY = 5

    def update(self):
        self.x += self.velX
        self.y += self.velY

    def setVelocity(self, newVelX, newVelY):
        self.velX = newVelX
        self.velY = newVelY

    def setPos(self, newX, newY):
        self.x = newX
        self.y = newY
        

class Brick:

    def __init__ (self, nx, ny):
        self.x = nx
        self.y = ny
    
    size = 90
    width = 15
    mass = 1
    borderColor = white
    fillColor = red
    
    x = res[0]/2 - size/2
    y = 70

    alive = True
    points = 10

    def update(self):
        pass

    def setAlive(self, newState):
        self.alive = newState

    def isAlive(self):
        return self.alive

    def getWidth(self):
        return self.width

    def getSize(self):
        return self.size

    def getPos(self):
        return (self.x, self.y)
    
    def setPos(self, newX, newY):
        self.x = newX
        self.y = newY


def gray (val):
    return pygame.Color(val,val,val)

# setup

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfObj = pygame.display.set_mode(res)
pygame.display.set_caption('brik')


fontSize = 24
fontObj = pygame.font.Font(None, fontSize)
label = 'Status: '
msg = 'Program started...'
title = 'brik'

game = Game()
game.setLevel(1)
player = Player(0,1)
paddle = Paddle()

mainBall = Ball(paddle.x + paddle.size/2, paddle.y - Ball.size)
mainBall.setVelocity(3,3)

# setup bricks
bricks = []

def setupBricks():
    global bricks

    for i in range(brickRows + game.getLevel()):
        for j in range(brickCols):
               bricks.append(Brick(res[0]/2 - (Brick.size*brickCols + brickPadding*(brickCols-1))/2 + j*(brickPadding + Brick.size), brickVertOffset + i*Brick.width + i*brickPadding))

setupBricks()


# input section
def processInput():
    global paused, msg, attached, paddle, debug
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == MOUSEMOTION:
            if not paused:
                 paddle.setPos(event.pos[0], paddle.y)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                leftClick()
            elif event.button == 2:
                middleClick()
            elif event.button == 3:
                rightClick()
            elif event.button == 4:
                scrollUp()
            elif event.button == 5:
                scrollDown()
                
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            elif event.key == K_p:
                paused = not paused
            elif event.key == K_n:
                nextLevel()
            elif event.key == K_d:
                debug = not debug
            elif event.key == K_SPACE:
                togglePause()

def pollInputs():
    global paddle

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        if not paused:
            paddle.setPos(paddle.x - paddle.velX, paddle.y)
    elif keys[K_RIGHT]:
        if not paused:
            paddle.setPos(paddle.x + paddle.velX, paddle.y)
    if keys[K_UP]:
        pass
    elif keys[K_DOWN]:
        pass

def leftClick():
    global msg, attached
    msg = 'left click'
    togglePause()

def rightClick():
    global msg
    msg = 'right click'

def middleClick():
    global msg
    msg = 'middle click'  

def scrollUp():
    global msg, mainBall
    msg = 'scroll up'
    if debug:
        mainBall.setVelocity(1.1*mainBall.velX, 1.1*mainBall.velY)
    
def scrollDown():
    global msg, mainBall
    msg = 'scroll down'
    if debug:
        mainBall.setVelocity(0.9*mainBall.velX, 0.9*mainBall.velY)

def togglePause():
    global paused
    paused = not paused
    pygame.mouse.set_visible(paused)
    
# graphics    
def draw():
    windowSurfObj.fill(black)

    # draw background
    drawBackground()
    
    # draw border
    pygame.draw.rect(windowSurfObj, white, (borderWidth,borderWidth,res[0]-borderWidth*2,res[1]-(fontSize + bottomPad + borderWidth*2)), 1)
    
    # draw ball
    pygame.draw.circle(windowSurfObj, white, mainBall.getPos(), mainBall.size)

    # draw paddle
    pygame.draw.rect(windowSurfObj, green, (paddle.x, paddle.y, paddle.size, paddle.width - paddle.notch))
    pygame.draw.rect(windowSurfObj, green, (paddle.x + paddle.notch, paddle.y, paddle.size - 2*paddle.notch, paddle.width))
    
    # draw bricks
    for brick in bricks:
        pygame.draw.rect(windowSurfObj, brick.fillColor, (int(brick.x), int(brick.y), brick.size, brick.width))
        pygame.draw.rect(windowSurfObj, brick.borderColor, (int(brick.x), int(brick.y), brick.size, brick.width), 2)
    
    # debug status
    if debug:
        drawText(windowSurfObj, label + msg, (10, res[1] - (fontSize)))
        drawText(windowSurfObj, 'Speed: ' + str(abs(mainBall.velX) + abs(mainBall.velY)), (res[0]/3, res[1] - (fontSize)))
    else:
        drawText(windowSurfObj, 'Lives: ' + str(player.getLives()), (borderWidth, res[1] - (fontSize)))
        
    # stats
    drawText(windowSurfObj, 'Score: ' + str(player.getPoints()), (res[0]*3/5 , res[1] - (fontSize)))
    drawText(windowSurfObj, 'Level: ' + str(game.getLevel()), (res[0]*4/5 , res[1] - (fontSize)))


def drawBackground():
    pygame.draw.circle(windowSurfObj, gray(25), (res[0]/3 + 40, res[1]/3), 240)
    pygame.draw.circle(windowSurfObj, gray(20), (res[0]*2/3, res[1]*2/3), 250)
    pygame.draw.circle(windowSurfObj, gray(15), (res[0]*1/4, res[1]*4/5), 200)

def drawText(wso, string, coords):
    textSurfObj = fontObj.render(string, False, white)
    textRectObj = textSurfObj.get_rect()
    textRectObj.topleft = coords
    wso.blit(textSurfObj, textRectObj)

def updatePositions():
    global mainBall
    if not paused:
        mainBall.update()
        

def checkCollision():
    global mainBall, paddle, bricks, player

    # check paddle
    if (paddle.x + paddle.size > res[0] - borderWidth):
        paddle.setPos(res[0] - paddle.size - borderWidth - 1, paddle.y)
    elif (paddle.x < borderWidth):
        paddle.setPos(borderWidth + 1, paddle.y)


    # check ball bounds
    # paddle
    if (mainBall.x > paddle.x and mainBall.x < paddle.x + paddle.size and mainBall.y > paddle.y - mainBall.size):
        mainBall.reflect('horz')
    # left and right edges
    if (mainBall.x < mainBall.size + borderWidth or mainBall.x > res[0] - mainBall.size - borderWidth):
        mainBall.reflect('vert')
    # top edge
    if (mainBall.y < mainBall.size + borderWidth):
        mainBall.reflect('horz')

    # bottom edge
    if (mainBall.y > res[1] - (borderWidth + bottomPad + fontSize + mainBall.size)):
        outOfBounds()

    
    # check all bricks with ball
    toRemove = []
    for brick in bricks:
        collision = brickBallCollision(mainBall, brick)
        if collision == 'horz':
            mainBall.reflect('horz')
            player.addPoints(brick.points)
            toRemove.append(brick)
            
        elif collision == 'vert':
            mainBall.reflect('vert')
            player.addPoints(brick.points)
            toRemove.append(brick)
            
        else:
            pass

    if toRemove != []:
        for brick in toRemove:
            bricks.remove(brick)

        
    
# given a ball and a brick, return whether they are colliding on the bricks vertical or horizontal surfaces or not at all
def brickBallCollision(ball, brick):
    collision = 'none'

    if (ball.x > brick.x and ball.x < brick.x + paddle.size and (ball.y < brick.y + brick.width + ball.size and ball.y > brick.y - ball.size)):
       collision = 'horz'


    if (ball.y > brick.y and ball.y < brick.y + brick.width):
        # within the vertical bounds of the brick

        # right edge
        if (ball.x < brick.x + brick.size + ball.size and ball.x > brick.x + brick.size/2):
            collision = 'vert'
        # left edge
        elif (ball.x + ball.size > brick.x  and ball.x + ball.size < brick.x + brick.size/2):
            collision = 'vert'
        
        
    return collision

def outOfBounds():
    global mainBall
    player.takeLife()
    if not paused:
        togglePause()
    resetPaddle()
    resetBall()

def checkGame():

    if bricks == []:
        nextLevel()
    if player.getLives() <= 0:
        resetGame()

def resetPaddle():
    global paddle
    paddle.setPos(res[0]/2 - paddle.size/2, paddle.y)

def resetBall():
    global mainBall
    mainBall.setPos(paddle.x + paddle.size/2, paddle.y - Ball.size)
    mainBall.setVelocity(3,3)
    
def nextLevel():
    global game

    game.setLevel(game.getLevel() + 1)
    setupBricks()

    if not paused:
        togglePause()
    resetPaddle()
    resetBall()

def resetGame():
    global game, player

    game.setLevel(1)
    setupBricks()

    if not paused:
        togglePause()
    resetPaddle()
    resetBall()
    
    player.setPoints(startingPoints)
    player.setLives(startingLives)

# main program loop
while True:

    # check status, lives, bricks, etc
    checkGame()
    
    # update positions
    updatePositions()
    checkCollision()
    
    # draw
    draw()
    
    # input
    processInput()
    pollInputs()

    # update draw
    pygame.display.update()
    fpsClock.tick(fps)

