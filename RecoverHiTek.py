# Mizatorian's Pygame community game
# Theme: High-Tech
#
# Idea is for a evil villain to break into a hi-tech factory, and throw all the high tech
# down a cliff. Your job as the fire-chief is to rescue and recover the items. 
# Player can move left/right to catch and bounce the items.

import pygame, os, sys, time
import random

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
        #self.image = pygame.Surface((60, 30))
        #self.image.fill(COLOR_GREEN)
        self.image = playerimage
        self.image.set_colorkey(COLOR_GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 - 70
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
        #self.image = pygame.Surface((30, 30))
        #self.image.fill(COLOR_BLUE)
        self.image = preciousimages[random.randrange(0,len(preciousimages))]
        self.image.set_colorkey(COLOR_GREEN)
        self.rect = self.image.get_rect()
        self.myx = self.rect.left = 100
        self.myy = self.rect.top = 30
        self.speedx = random.randrange(10,13)/10
        #self.speedx = 1
        self.speedy = 0
        self.accely = 0.1
        #print("Speedx",self.speedx)

    def update(self):
        global score, gameover, ismenu, PRECIOUSINTERVAL
        self.myx += self.speedx
        self.speedy += self.accely
        if self.speedy > MAXYSPEED : self.speedy = MAXYSPEED
        self.myy += self.speedy
        self.rect.left = self.myx
        self.rect.top = self.myy
        
        if self.rect.right > WIDTH:
            self.kill()
            score += 1
            scoresound.play()
            PRECIOUSINTERVAL = clip(PRECIOUSINTERVAL-0.1,5,10)
        if pygame.sprite.collide_rect(player, self):
            #Collided with the player, hence must bounce up
            self.speedy = -abs(self.speedy) + 0.25
            bouncesound.play()
        if self.rect.bottom > HEIGHT - 10 :
            self.rect.bottom = 0
            gameover=True
            ismenu = True
            ohohsound.play()
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
PRECIOUSINTERVAL = 7
MAXYSPEED=7.5
FPS = 30


screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
gamescreen = pygame.Surface(WINDOW_SIZE) 
menuscreen   = pygame.Surface(WINDOW_SIZE) 
score = 0

assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
bgimage = pygame.image.load(os.path.join(assets_dir, 'bg.png')).convert()
bg_rect = bgimage.get_rect()
bgmenuimage = pygame.image.load(os.path.join(assets_dir, 'bgmenu.png')).convert()
bgmenu_rect = bgimage.get_rect()
playerimage = pygame.image.load(os.path.join(assets_dir, 'player.png')).convert()
preciousimages=[]
for i in range(1,7):
    temp = pygame.image.load(os.path.join(assets_dir, 'hitek'+str(i)+'.png')).convert()
    preciousimages.append(temp)

bouncesound = pygame.mixer.Sound(os.path.join(assets_dir, "sfxr_bounce.wav"))
ohohsound  = pygame.mixer.Sound(os.path.join(assets_dir, "sfxr_ohoh3.wav"))
scoresound  = pygame.mixer.Sound(os.path.join(assets_dir, "sfxr_score.wav"))


while True:
    inmenu=True
    gameover=False

    font = pygame.font.Font('at01.ttf', 32)
    all_sprites = None
    all_sprites = pygame.sprite.Group()
    player = Player()
    precious = Precious()
    all_sprites.add(player)
    all_sprites.add(precious)
    precioustimer = time.time()
    pygame.mixer.music.load(os.path.join(assets_dir, "guitar1.mp3"))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    while not gameover: # main game loop

        # Do event loop processing first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and inmenu == True:
                    inmenu = False
                    precioustimer = time.time()
                    pygame.mixer.music.set_volume(0.3)
                    score = 0

        # Do update 
        if not inmenu:
            #gamescreen.fill(COLOR_GRAY1) # Grey background
            gamescreen.blit(bgimage, bg_rect)
            # Game Play code here
            all_sprites.update()

            #Check if item collided with the player, if so bounce

            all_sprites.draw(gamescreen)
            #Debug Precious
            text = font.render('Score: ' + str(score), True, COLOR_BLACK)
            textRect = text.get_rect()
            textRect.center = (500,20)
            textRect.right=550
            precioustimer = checktimeforprecious(precioustimer)
            gamescreen.blit(text, textRect)

            screen.blit(pygame.transform.scale(gamescreen,WINDOW_SIZE),(0,0))

        if inmenu:
            menuscreen.blit(bgmenuimage, bgmenu_rect)
            # menu screen
            textlist = ["Mizatorian's PyGame Community Jam",
                        " ",
                        "------>> Recover HI-TEK <<------",
                        " ",
                        "The evil villain Gazmodo has infiltrated Hi-TEK and is",
                        "destroying all the high-tech gadgets by throwing them",
                        "off the HI-TEK tower. As the response chief, your job",
                        "is to save all the hi-tek items from being destroyed.",
                        " ",
                        "LEFT Arrow = move left",
                        "RIGHT Arrow = move right",
                        "Q = Quit",
                        " ",
                        "Press SPACE to start"," ",
                        ("Last Score: "+str(score) if score>0 else " ")
                        ]
            start = 60
            for item in textlist:
                text = font.render(item, True, COLOR_WHITE)
                textRect = text.get_rect()
                textRect.center = (300,start)
                start += 25
                menuscreen.blit(text, textRect)

            screen.blit(pygame.transform.scale(menuscreen,WINDOW_SIZE),(0,0))

        pygame.display.update()
        clock.tick(FPS)