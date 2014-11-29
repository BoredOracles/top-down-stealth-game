__author__ = '2091723f'

import pygame, sys, time, copy, math
from pygame.locals import *

# controls list [up,left,down,right,sneak,space]

def rot_center(image, angle):
    """rotate an image while keeping its center and size from http://www.pygame.org/wiki/RotateCenter?parent=CookBook"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Player(pygame.sprite.Sprite):


    def __init__(self, group, controls=[K_w, K_a, K_s, K_d, K_LSHIFT, K_SPACE]):
        pygame.sprite.Sprite.__init__(self)
        self.controls = controls
        self.direction = 0
        self.position = [100, 100]
        self.dx = 0
        self.dy = 0
        self.moveSpeed = 5
        self.sneak = False
        self.moveTimer = time.clock()
        self.pauseTime = .05
        self.avatar = pygame.image.load("playerPNG.png").convert_alpha()
        Player.rect = pygame.Rect(self.position[0] + 2, self.position[1] + 14, 46, 22)
        self.rect = pygame.Rect(self.position[0] + 2, self.position[1] + 14, 46, 22)
        self.sneakConstant = .5
        self.currentMap = None

    def rectUpdate(self):
        Player.rect = pygame.Rect(self.position[0] + 2, self.position[1] + 14, 46, 22)

    def move(self):
        if time.clock() - self.moveTimer >= self.pauseTime:
            if self.sneak:
                self.position = [self.position[0] + (self.dx * self.sneakConstant),
                                 self.position[1] + (self.dy * self.sneakConstant)]
            else:
                self.position = [self.position[0] + self.dx, self.position[1] + self.dy]
            self.moveTimer = time.clock()
            player.rectUpdate()

            #TODO : update direction and Rect


class Controller:
    def __init__(self):
        self.queue = []
        self.pressedKeys = []

    def quitTest(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    def checkControl(self, direction, forward):
        if (forward == 1) and (not direction < 0):
            return True
        elif (forward == -1) and (not direction > 0):
            return True
        return False

    def queueRetrieve(self, key):
        for event in self.queue:
            if event.key == key:
                self.interpretEvent(event, player)
                self.queue.pop(self.queue.index(event))

    def interpretEvent(self, event, player):
        self.quitTest(event)
        if event.type == KEYDOWN and event.key in player.controls:
            if event.key not in self.pressedKeys:
                self.pressedKeys.append(event.key)
            if event.key == player.controls[4]:
                player.sneak = True
            elif event.key == player.controls[5]:
                if player.currentMap.item is not None:
                    singleItem = pygame.sprite.GroupSingle(player.currentMap.item)
                    if pygame.sprite.spritecollide(Player, singleItem, False) != []:
                        player.currentMap.item.interact(player)
                        player.currentMap.item = None
            else:
                positives = [-1, -1, 1, 1]
                directions = [player.dy, player.dx, player.dy, player.dx]
                if self.checkControl(directions[player.controls.index(event.key)],
                                     positives[player.controls.index(event.key)]):
                    if player.controls.index(event.key) in (0, 2):
                        player.dy = positives[player.controls.index(event.key)] * player.moveSpeed
                    elif player.controls.index(event.key) in (1, 3):
                        player.dx = positives[player.controls.index(event.key)] * player.moveSpeed
                elif event not in self.queue:
                    self.queue.append(event)
        elif event.type == KEYUP and event.key in player.controls:
            if event.key in self.pressedKeys:
                self.pressedKeys.pop(self.pressedKeys.index(event.key))

            for queueEvent in self.queue:
                if queueEvent.key == event.key:
                    self.queue.pop(self.queue.index(queueEvent))

            if event.key in (player.controls[0], player.controls[2]):
                if (player.controls[(player.controls.index(event.key) + 2) % 4]) not in self.pressedKeys:
                    player.dy = 0
                else:
                    self.queueRetrieve(player.controls[(player.controls.index(event.key) + 2) % 4])

            elif event.key in (player.controls[1], player.controls[3]):
                if (player.controls[(player.controls.index(event.key) + 2) % 4]) not in self.pressedKeys:
                    player.dx = 0
                else:
                    self.queueRetrieve(player.controls[(player.controls.index(event.key) + 2) % 4])
            elif event.key == player.controls[4]:
                player.sneak = False


class Item(pygame.sprite.Sprite):
    def __init__(self, interact, position, avatar):
        pygame.sprite.Sprite.__init__(self)
        self.interact = interact
        self.position = position
        self.avatar = avatar
        self.rect = pygame.Rect(self.position[0],self.position[1],50,50)


def putOnSneakers(player):
    player.sneakConstant = 2


class Map:
    def __init__(self, item):
        self.item = item
        self.item = item


def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


pygame.init()  #starts pygame
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

sampleJPG = pygame.image.load("sampleJPG.jpg").convert()
fontName = "default"
fontSize = 30
textFont = pygame.font.SysFont(fontName, fontSize)

playerSpriteGroup = pygame.sprite.Group()

sneakers = Item(putOnSneakers, [200, 200], pygame.image.load("playerPNG.png").convert_alpha())

player = Player(group=playerSpriteGroup)
player.currentMap = Map(sneakers)

controller = Controller()

while True:
    event = pygame.event.poll()
    controller.interpretEvent(event, player)

    player.move()
    screen.blit(sampleJPG, (0, 0))
    if player.currentMap.item is not None:
        screen.blit(player.currentMap.item.avatar,
                    (player.currentMap.item.position[0], player.currentMap.item.position[1]))
    screen.blit(rot_center(player.avatar, player.direction), (player.position[0], player.position[1]))
    pygame.display.update()
