##MIT License
##
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:
##
##The above copyright notice and this permission notice shall be included in all
##copies or substantial portions of the Software.
##
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

##Version 0.1
##March 2017
##Author...

import pygame
import sys
from pygame.locals import *
import time
import random

background=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,225)
special=1
level=50
create=level
Asteroids=[]
SpecialRock=[]
Lasers=[]
lives=3
score=0

class Player(pygame.sprite.Sprite):
    """The player controlled Ship"""

    def __init__(self, x,y,width,height):
        pygame.sprite.Sprite.__init__(self)

        self.x=x
        self.y=y
        self.width=width
        self.height=height

        self.image=pygame.Surface((self.width,self.height))
        self.image.fill(background)

        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.y_change=0
        
    def MoveKeyDown(self,key):
        if key == K_RIGHT: #if key right is pushed, shoot laser
            shooting.play(0) #play sound
            laser=Shoot(ship.rect.x + 74, ship.rect.y + 36, 10, 5)
            all_sprites_list.add(laser)
            Lasers.append(laser)
        elif key==K_DOWN: #if key down is pushed, go down
            self.y_change += 5
        elif key==K_UP: #if key up is pushed, go up
            self.y_change += -5

    def MoveKeyUp(self,key):
        if key==K_UP: #if key up is lifted
            self.y_change += 5
        elif key==K_DOWN: #if key down is lifted
            self.y_change += -5
            
    def update(self):
        self.rect.move_ip(0, self.y_change)

        #ship borders
        if self.rect.y<0:
            self.rect.y=0
            move=False
        elif self.rect.y>500-74:
            self.rect.y=500-74
            move=False

        #for debugging --> print(self.rect.y)
        DISPLAYSURF.fill(background)
        DISPLAYSURF.blit(spaceship, (0, self.rect.y))

class Shoot(Player):
    def __init__(self, x,y,width,height):
        super(Shoot, self).__init__(x,y,width,height)
        self.speed=3
        self.speed=1

        self.image=pygame.Surface((5,2))
        self.image.fill(WHITE)

        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)

##    def check(self,bullet):
##        if bullet:
##            self.x+=2
##            DISPLAYSURF.blit(laserbeam, (self.x, self.y))
##            if self.x>600:
##                bullet=False
    
    def update(self):
        #keep laser moving
        self.rect.x+=5

#asteroid class
class Rocks(Player):
    def __init__(self, x,y,width,height):
        super(Rocks, self).__init__(x,y,width,height)

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.x_direction = 1
        self.speed = 3

    def update(self):
        self.rect.x-=5

#special asteroid class
class LIFE(Player):
    def __init__(self, x,y,width,height):
        super(LIFE, self).__init__(x,y,width,height)

        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        self.x_direction = 1
        self.speed = 3

    def update(self):
        self.rect.x-=5

def check(rocks):
    global level
    global create
    global lives
    global score
    global special

    listscore=[]
    #for everything in Asteroids
    for r in rocks:
        #if there is collision, remove from sprite group and list, subtract lives
        if r.rect.colliderect(ship.rect):
            special=1
            shipcollide.play()
            rocks.remove(r)
            all_sprites_list.remove(r)
            lives-=1
            print('LIVES: '+str(lives))
            #blit lives onto screen
            end_it = False
            while (end_it == False):
                font = pygame.font.Font(None, 36)
                text = font.render(str(lives), 1, (WHITE))
                textpos = text.get_rect(centerx=DISPLAYSURF.get_width()/2)
                DISPLAYSURF.blit(text, textpos)
                end_it=True

        #if lives is at 0
        if lives==0:
            endgame.play()
            time.sleep(3)
            endgame.stop()
            #save highscore
            file=open('highscores.txt','r')
            for line in file:
                listscore.append(int(line))
            listscore.append(score)
            listscore=sorted(listscore, reverse=True)
            file.close()
            
            #if len of scores is greater than 10, make it 10
            if len(listscore)>10:
                del listscore[-1]

            #write list to file to update scores
            file=open('highscores.txt','w')
            for i in listscore:
                file.write(str(i)+'\n')
            file.close()

            #game over
            all_sprites_list.remove(all)
            end_it=False
            while (end_it==False):
                #blit game over on screen
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 45)
                overobj = textbasics.render('Game Over', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx
                overrect.centery = DISPLAYSURF.get_rect().centery-45
                DISPLAYSURF.blit(overobj,overrect)

                #blit the score
                scoreobj=textbasics.render(str(score),True,RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj,scorerect)

                #if score in list, its in top 10
                if score in listscore:
                    topobj=textbasics.render("TOP 10!", True, RED)
                    toprect=topobj.get_rect()
                    toprect.centerx = DISPLAYSURF.get_rect().centerx
                    toprect.centery = DISPLAYSURF.get_rect().centery+45
                    DISPLAYSURF.blit(topobj,toprect)
                    
                for event in pygame.event.get():
                    if event.type==pygame.QUIT: #if exed out
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

def collision(laz,rocks):
    global score
    #for everything in Lasers
    for l in laz:
        #for everything in Asteroids
        for r in rocks:
            #if there is a collision
            if l.rect.colliderect(r):
                #play sound
                astcollide.play()
                #remove from list and sprite group, add to score
                rocks.remove(r)
                all_sprites_list.remove(r)
                laz.remove(l)
                all_sprites_list.remove(l)
                score+=100
                #blit score onto screen
                end_it = False
                while (end_it == False):
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(score), 1, (WHITE))
                    textpos = text.get_rect(centerx=DISPLAYSURF.get_width()/2)
                    DISPLAYSURF.blit(text, textpos)
                    print('SCORE: '+str(score))
                    end_it=True
            if r.rect.x<=0:
                #if asteroids is less than x=0, remove from sprite group, subtract from score
                rocks.remove(r)
                all_sprites_list.remove(r)
                score-=100
                #blit score onto screen
                end_it=False
                while (end_it==False):
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(score), 1, (WHITE))
                    textpos = text.get_rect(centerx=DISPLAYSURF.get_width()/2)
                    DISPLAYSURF.blit(text, textpos)
                    print('SCORE: '+str(score))
                    end_it=True

def specialcollision(laz,special):
    global lives
    for l in laz: #for every lazor
        for s in special: #for every special asteroid
            if l.rect.colliderect(s): #if collided, make noise and remove asteroid and laserfrom screen
                astcollide.play()
                special.remove(s)
                all_sprites_list.remove(s)
                laz.remove(l)
                all_sprites_list.remove(l)
                lives+=1
                #blit lives onto screen
                end_it = False
                while (end_it == False):
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(lives), 1, (WHITE))
                    textpos = text.get_rect(centerx=DISPLAYSURF.get_width()/2)
                    DISPLAYSURF.blit(text, textpos)
                    print('LIVES: '+str(lives))
                    end_it=True
            if s.rect.x<=0:
                #if asteroid is less than x=0, remove from sprite group, subtract from score
                special.remove(s)
                all_sprites_list.remove(s)

#set screen
pygame.init()
pygame.mixer.init()
screenwidth=600
screenheight=500
DISPLAYSURF=pygame.display.set_mode((600,500))
pygame.display.set_caption('Asteroid Shooting Game')

#load image/sound
spaceship=pygame.image.load('ship.png')
shooting=pygame.mixer.Sound('bullet.wav')
astcollide=pygame.mixer.Sound('asteroidhit.wav')
shipcollide=pygame.mixer.Sound('shipblowup.wav')
endgame=pygame.mixer.Sound('gameover.wav')
#background music
bgmusic=pygame.mixer.Sound('Deep-in-space-120-bpm.wav')
bgmusic.play(-1,0)
bgmusic.set_volume(0.07)

#ship/player info
ship=Player(0,screenwidth/2,0,0)
all_sprites_list=pygame.sprite.Group()
all_sprites_list.add(ship)

fpsClock = pygame.time.Clock()

#start screen
end_it=False
while (end_it==False):
    #get font
    text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)

    #title font, blit in center
    titleobj = text.render('Asteroid Shooting Game', True, WHITE)
    titlerect = titleobj.get_rect()
    titlerect.centerx = DISPLAYSURF.get_rect().centerx
    titlerect.centery = DISPLAYSURF.get_rect().centery-90
    DISPLAYSURF.blit(titleobj,titlerect)

    #start game font, blit in center
    startobj = text.render('Start Game', True, RED)
    startrect = startobj.get_rect()
    startrect.centerx = DISPLAYSURF.get_rect().centerx
    startrect.centery = DISPLAYSURF.get_rect().centery-45
    DISPLAYSURF.blit(startobj, startrect)

    #open file to find highscore and blit on screen
    scores=[]
    file=open('highscores.txt','r')
    for line in file:
        scores.append(int(line))
    file.close()
    scoreobj=text.render("Highscore: "+str(scores[0]), True, WHITE)
    scorerect = scoreobj.get_rect()
    scorerect.centerx = DISPLAYSURF.get_rect().centerx
    scorerect.centery = DISPLAYSURF.get_rect().centery
    DISPLAYSURF.blit(scoreobj, scorerect)

    #instructions, blit to start screen
    moveobj = text.render('Use arrows to move up and down', True, BLUE)
    moverect = moveobj.get_rect()
    moverect.centerx = DISPLAYSURF.get_rect().centerx
    moverect.centery = DISPLAYSURF.get_rect().centery+45
    DISPLAYSURF.blit(moveobj, moverect)
    shootobj = text.render('Use right arrow to shoot', True, BLUE)
    shootrect = shootobj.get_rect()
    shootrect.centerx = DISPLAYSURF.get_rect().centerx
    shootrect.centery = DISPLAYSURF.get_rect().centery+90
    DISPLAYSURF.blit(shootobj, shootrect)

    for event in pygame.event.get():
        #if mousebuttondown or space pressed start game
        if event.type==MOUSEBUTTONDOWN:
            end_it=True
        #if quit, exit
        elif event.type==pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
    pygame.display.flip()

#start game
while True:
    collision(Asteroids,Lasers) #check for collisions
    specialcollision(Lasers,SpecialRock)
    check(Asteroids) #check for asteroids

    #create new astroid
    if create<=0:
        rock = Rocks(screenwidth, random.randint(0,screenheight), 20, 20)
        all_sprites_list.add(rock)
        Asteroids.append(rock)
        level-=1
        create=level
    if special==1:
        #create special asteroid
        rock = LIFE(screenwidth, random.randint(0,screenheight), 20, 20)
        all_sprites_list.add(rock)
        SpecialRock.append(rock)
        special-=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit pygame
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN: #if key is pressed
            ship.MoveKeyDown(event.key) #go to this function
            ship.update()
        elif event.type == pygame.KEYUP: #if key is up
            ship.MoveKeyUp(event.key) #go to this function
            ship.update()

    for ent in all_sprites_list: #update all
        ent.update()

    all_sprites_list.draw(DISPLAYSURF) #draw all sprites

    create-=1 #subtract to create astroids

    pygame.display.flip() #flip screen

    fpsClock.tick(30)
