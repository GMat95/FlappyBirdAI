import pygame
import neat
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))), 
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))), 
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VELOTCITY = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.tilt = 0
        self.tickCount = 0
        self.velocity = 0
        self.height = self.y
        self.imgCount = 0
        self.img = self.IMGS[0]
        
    def jump(self):
        self.velocity = -10.5
        self.tickCount = 0
        self.height = self.y
    
    def move(self):
        self.tickCount += 1
        displacement = self.velocity * self.tickCount + 1.5 * self.tickCount ** 2
        
        if displacement >= 16:
            displacement = 16
            
        if displacement < 0:
            displacement -= 2
            
        self.y = self.y + displacement
        
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VELOTCITY
            
            
    def draw(self, win):
        self.imgCount += 1
        
        if self.imgCount < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.imgCount < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.imgCount < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.imgCount < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.imgCount == self.ANIMATION_TIME*4 + 1: 
            self.img = self.IMGS[0]
            self.imgCount = 0
            
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.imgCount = self.ANIMATION_TIME*2
        
        #Rotate the self.img around the center instead or around top    
        rotatedImg = pygame.transform.rotate(self.img, self.tilt)
        newRect = rotatedImg.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotatedImg, newRect.topleft)
        
    def getMask(self):
        return pygame.mask.from_surface(self.img)
    
    
def drawWindow(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()
        
def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        drawWindow(win, bird)
    
    pygame.quit()
    quit()
    
main()
                