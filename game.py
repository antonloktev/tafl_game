import pygame, sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((400,400),pygame.RESIZABLE,32)
pygame.display.set_caption("My First PyGame Windows")

helloText = "Hello, World and GCUP"
(x,y, fontSize) = (10,40,30)

myFont = pygame.font.Font("D:\\Torrents\\freesansbold.ttf", fontSize)
fontColor = (255,0,0)
bgColor = (255, 255, 255)
bgImage = pygame.image.load("board.png")
fontImage = myFont.render(helloText, True, (fontColor))

mainLoop = True
while mainLoop:
    for event in pygame.event.get():
        if event.type == QUIT:
            mainLoop = False
    screen.fill(bgColor)
    screen.blit(bgImage, (50,50))
    pygame.display.update()
pygame.quit()