#Voltorb Flip
#Made by Andrew Kang

#yo

import pygame
from pygame import *
from random import choice

#set odds for value choice
# 1: 8/14  2: 2/14  3: 1/14  Bomb: 3/14
ODDS = [1,1,1,1,1,1,1,1,2,2,3,0,0,0]

#create list for tiles worth more than 1 point
VALUETILES = []

#create list for bomb tiles
VOLTORBS = []

#create display window
SCREEN_WIDTH = 655
SCREEN_HEIGHT = 998

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Voltorb Flip')

#load images
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (655,998)).convert()
blankTile = pygame.image.load('assets/blanktile.png')
blankTile = pygame.transform.scale(blankTile, (60,60)).convert()
flippedTile1 = pygame.image.load('assets/flippedtile1.png')
flippedTile1 = pygame.transform.scale(flippedTile1, (60,60)).convert()
flippedTile2 = pygame.image.load('assets/flippedtile2.png')
flippedTile2 = pygame.transform.scale(flippedTile2, (60,60)).convert()
flippedTile3 = pygame.image.load('assets/flippedtile3.png')
flippedTile3 = pygame.transform.scale(flippedTile3, (60,60)).convert()
hoverTile = pygame.image.load('assets/tilehover.png')
hoverTile = pygame.transform.scale(hoverTile, (75,75)).convert()
bombTile = pygame.image.load('assets/bombtile.png')
bombTile = pygame.transform.scale(bombTile, (60,60)).convert()

boldNums = []
for i in range(10):
    tempNum = pygame.image.load('assets/bold_' + str(i) + '.png')
    tempNum = pygame.transform.scale(tempNum, (15,20)).convert()
    boldNums.append(tempNum)

bigNums = []
for i in range(10):
    tempNum = pygame.image.load('assets/big_' + str(i) + '.png')
    tempNum = pygame.transform.scale(tempNum, (35,55)).convert()
    bigNums.append(tempNum)



#set starting points amount
TOTALMONEY = 0
TOTALDISPLAY = '00000'
MONEY = 1
MONEYDISPLAY = '00000'

def flipCheck():
    global cardGrid
    win = True
    for i in range(5):
        for t in range(5):
            if cardGrid[i][t].value > 1 and cardGrid[i][t].flipped == False:
                win = False
    return win


class Card():
    def __init__(self, x, y, image, value):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.flipped = False
        self.value = value
    
    #draw card onto screen
    def draw(self):
        #get mouse pos
        pos = pygame.mouse.get_pos()
        
        #print(pos)
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            #Shows hover graphic
            screen.blit(hoverTile, (self.rect.x - 8, self.rect.y - 8))
            

            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                self.clicked = True
                if self.flipped == False:
                    self.flipCard()
        
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
            


        screen.blit(self.image, (self.rect.x, self.rect.y))

    
    
    def flipCard(self):
        global run, MONEY, MONEYDISPLAY
        lost = False
        self.flipped = True
        if self.value == 0:
            self.image = bombTile
            lost = True
        elif self.value == 1:
            self.image = flippedTile1
        elif self.value == 2:
            self.image = flippedTile2
        else:
            self.image = flippedTile3
        MONEY *= self.value
        MONEYDISPLAY = str(MONEY)
        while len(MONEYDISPLAY) < 5:
            MONEYDISPLAY = '0' + MONEYDISPLAY
        if lost:
            MONEY = 1
            makeBoard()
        

def makeBoard():
    global cardGrid, horPoints, verPoints, horVoltorbs, verVoltorbs

    #create Card instances (5x5 Grid)
    cardGrid = []
    for i in range(5):
        tempList = []
        for t in range(5):
            tempVal = choice(ODDS)
            tempVar = Card(28 + (t * 80), 508 + (i * 80), blankTile, tempVal)
            tempList.append(tempVar)
            if tempVal < 1:
                VOLTORBS.append(tempVar)
            elif tempVal > 1:
                VALUETILES.append(tempVar)
        cardGrid.append(tempList)

    #Count points in a row
    horPoints = []
    for i in range(5):
        tempSum = 0
        for t in range(5):
            tempSum += cardGrid[i][t].value
        tempSum = str(tempSum)
        if len(tempSum) == 1:
            tempSum = '0' + tempSum
        horPoints.append(tempSum)

    #Count points in a column
    verPoints = []
    for i in range(5):
        tempSum = 0
        for t in range(5):
            tempSum += cardGrid[t][i].value
        tempSum = str(tempSum)
        if len(tempSum) == 1:
            tempSum = '0' + tempSum
        verPoints.append(tempSum)

    #Count voltorbs in a row
    horVoltorbs = []
    for i in range(5):
        tempSum = 0
        for t in range(5):
            if cardGrid[i][t].value == 0:
                tempSum += 1
        horVoltorbs.append(tempSum)

    #Count voltorbs in a column
    verVoltorbs = []
    for i in range(5):
        tempSum = 0
        for t in range(5):
            if cardGrid[t][i].value == 0:
                tempSum += 1
        verVoltorbs.append(tempSum)



makeBoard()

#game loop
run = True
clock = pygame.time.Clock()
while run:
    clock.tick(30)

    #set background
    screen.blit(background,(0,0))


    #display total points earned
    for i in range(5):
        screen.blit(bigNums[int(TOTALDISPLAY[i])], (430 + (i * 40), 293))


    #display current points earned
    for i in range(5):
        screen.blit(bigNums[int(MONEYDISPLAY[i])], (430 + (i * 40), 393))


    #display points in row/column
    for i in range(5):
        #rows
        screen.blit(boldNums[int(horPoints[i][0])],(449, 508 + (i * 80)))
        screen.blit(boldNums[int(horPoints[i][1])],(469, 508 + (i * 80)))
        #columns
        screen.blit(boldNums[int(verPoints[i][0])],(49 + (i * 80), 908))
        screen.blit(boldNums[int(verPoints[i][1])],(69 + (i * 80), 908))

    #display amount of voltorbs in row/column
    for i in range(5):
        screen.blit(boldNums[horVoltorbs[i]],(469, 543 + (i * 80)))
        screen.blit(boldNums[verVoltorbs[i]], (69 + (i * 80),942))

    #load images in loop
    for i in range(5):
        for t in range(5):
            cardGrid[i][t].draw()
    

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    if flipCheck():
        print('You win!')
        pygame.time.delay(5000)
        TOTALMONEY += MONEY
        MONEY = 1
        DISPLAYMONEY = '00000'
        TOTALDISPLAY = str(TOTALMONEY)
        while len(TOTALDISPLAY) < 5:
            TOTALDISPLAY = '0' + TOTALDISPLAY
        
        makeBoard()

    pygame.display.update()

    