import pygame
from pygame.locals import *

#simple pygame methods

pygame.init() #starts pygame
screenWidth = 1400
screenHeight = 1000
screen = pygame.display.set_mode((screenWidth, screenHeight))

fontName = "default"
fontSize = 30
textFont = pygame.font.SysFont(fontName,fontSize)

try:
    sampleJPG = pygame.image.load("sampleJPG.jpg").convert()
    #JPGs are more performant but lack alpha pixels
except:
    print "could not find sample JPG"

try:
    samplePNG = pygame.image.load("samplePNG.png").convert_alpha()
    #PNGs have alpha (transparent) pixels - good for images that are not squares
except:
    print "could not find sample PNG"

def quitTest(event): #this should be always checked when looking at events - it makes the red topright x work
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

while True: #game loop
    event = pygame.event.poll()
    #takes the first event from the pygame event queue
    if event.type == KEYDOWN:
        if event.key == K_w:
            text = "the W key is down"
            antiAlias = 1
            color = (255,255,255) #white
            position = (100,100) #measured from top-left
            screen.blit(textFont.render(text,antiAlias,color),position)
    elif event.type == KEYUP:
        if event.key == K_w:
            screen.blit(sampleJPG,(0,0))
    quitTest(event)
    pygame.display.update() #updates the screen to show whats been blitted
    
    
