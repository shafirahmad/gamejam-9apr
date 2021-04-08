# Mizatorian's Pygame community game
# Theme: High-Tech
#
# Idea is for a evil villain to break into a hi-tech factory, and throw all the high tech
# down a cliff. Your job as the fire-chief is to rescue and recover the items. 
# Player can move left/right to catch and bounce the items.

import pygame, os, sys, time
import math, random

def clip(x, min, max) :
    if( min > max ) :  return x    
    elif( x < min ) :  return min
    elif( x > max ) :  return max
    else :             return x

def checktimeforprecious(precioustimer):
    if time.time() - precioustimer > PRECIOUSINTERVAL:
        precious = Precious()    
        all_sprites.add(precious)
        return time.time()

    return precioustimer


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 30))
        self.image.fill(COLOR_GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -PLAYERSPEED
        if keystate[pygame.K_RIGHT]:
            self.speedx = PLAYERSPEED
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Precious(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(COLOR_BLUE)
        self.rect = self.image.get_rect()
        self.myx = self.rect.left = 100
        self.myy = self.rect.top = 30
        #self.speedx = random.randrange(10,12)/10
        self.speedx = 1
        self.speedy = 0
        self.accely = 0.1
        print("Speedx",self.speedx)

    def update(self):
        global score, gameover
        self.myx += self.speedx
        self.speedy += self.accely
        if self.speedy > MAXYSPEED : self.speedy = MAXYSPEED
        self.myy += self.speedy
        self.rect.left = self.myx
        self.rect.top = self.myy
        
        if self.rect.right > WIDTH:
            self.kill()
            score += 1
        if pygame.sprite.collide_rect(player, self):
            #Collided with the player, hence must bounce up
            self.speedy = -abs(self.speedy) + 0.25
        if self.rect.bottom > HEIGHT - 10 :
            self.rect.bottom = 0
            gameover=True
            # died, hit the ground
    

clock = pygame.time.Clock()

pygame.init() 
pygame.display.set_caption('Mizatorian Apr2020 High-Tech Recovery')

HEIGHT=480
WIDTH=600
WINDOW_SIZE = (WIDTH,HEIGHT)

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_RED = (255,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)
COLOR_YELLOW = (255,255,0)
COLOR_GRAY1 = (90,90,90)
COLOR_GRAY2 = (190,190,190)
COLOR_GRAY3 = (120,120,120)
PLAYERSPEED = 15
PRECIOUSINTERVAL = 5
MAXYSPEED=6
FPS = 30

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
gamescreen = pygame.Surface(WINDOW_SIZE) 
menuscreen   = pygame.Surface(WINDOW_SIZE) 

while True:
    inmenu=False
    gameover=False
    moving_right = False
    moving_left = False
    score = 0

    font = pygame.font.Font('at01.ttf', 32)
    all_sprites = pygame.sprite.Group()
    player = Player()
    precious = Precious()
    all_sprites.add(player)
    all_sprites.add(precious)
    precioustimer = time.time()

    while not gameover: # main game loop

        # Do event loop processing first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Do update 
        if not inmenu:
            gamescreen.fill(COLOR_GRAY1) # Grey background
            # Game Play code here
            all_sprites.update()

            #Check if item collided with the player, if so bounce

            all_sprites.draw(gamescreen)
            #Debug Precious
            text = font.render( 'Y: ' + str(precious.rect.y) +
                                ' Acc:' + str(precious.accely) +
                                ' Sp:' + str(precious.speedy) +
                                ' Sc:' + str(score), True, COLOR_BLACK, COLOR_GRAY2 )
            textRect = text.get_rect()
            textRect.center = (200,20)
            precioustimer = checktimeforprecious(precioustimer)
            if 0: print('Y: ' + str(precious.rect.y) +
                                ' Acc:' + str(precious.accely) +
                                ' Sp:' + str(precious.speedy) +
                                ' Sc:' + str(score) )
            gamescreen.blit(text, textRect)

            screen.blit(pygame.transform.scale(gamescreen,WINDOW_SIZE),(0,0))

        if inmenu:
            menuscreen.fill(COLOR_BLUE) # Grey background
            # menu screen
            screen.blit(pygame.transform.scale(menuscreen,WINDOW_SIZE),(0,0))

        pygame.display.update()
        clock.tick(FPS)