import pygame
import sys
import os
import math
import random     

game_active = False
wcooldown = 0

dir = os.path.dirname(__file__)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Screen size constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

w = (SCREEN_WIDTH/2 + SCREEN_WIDTH/9) - (SCREEN_WIDTH/2 - SCREEN_WIDTH/9)
h = (SCREEN_HEIGHT/2 + SCREEN_HEIGHT/12) - (SCREEN_HEIGHT/2 - SCREEN_HEIGHT/12)   

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pong")

buttongroup = pygame.sprite.Group()

class Button(pygame.sprite.Sprite):
    global w
    global h
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (int(w), int(h)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2

img_dir = os.path.join(dir, 'pongimages')  

button_image = pygame.image.load(os.path.join(img_dir, 'button.png')).convert()  
button_rect = button_image.get_rect()

board_image = pygame.image.load(os.path.join(img_dir, 'board.png')).convert()  
board_rect = board_image.get_rect()

ball_image = pygame.image.load(os.path.join(img_dir, 'ball.png')).convert()  
ball_rect = button_image.get_rect()

def display_text(surf, text, size, color, x, y):
    font = pygame.font.SysFont("serif", size)      
    text_surface = font.render(text, True, color) 
    text_rect = text_surface.get_rect()           
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Paddle(pygame.sprite.Sprite):
    # Sprite class for the player
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = SCREEN_HEIGHT - 75
        
    def update(self):
        self.speedx = 0
        self.speedy = 0
        # If left or right key is pressed, move left or right
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_LEFT]: 
            self.speedx = -13
        if pressed_key[pygame.K_RIGHT]:
            self.speedx = 13
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Ball(pygame.sprite.Sprite):
    # Sprite class for the mobs
    def __init__(self, x, y, size, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (size, size))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        global speedx
        global speedy
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            speedx*=-1
        if self.rect.left < 0:
            self.rect.left = 0
            speedx*=-1
        if self.rect.top < 0:
            self.rect.top = 0
            speedy*=-1              
        self.rect.x += speedx
        self.rect.y += speedy

speedx = 6
speedy = 6
addable = True

screen.fill(BLACK)
display_text(screen, "Pong", 120, YELLOW, SCREEN_WIDTH//2, SCREEN_HEIGHT//5)

def startbutton(text):
    button = Button(button_image)
    buttongroup.add(button)
    buttongroup.draw(screen)
    display_text(screen, text, 25, WHITE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2-15)
    pygame.display.flip()

startbutton("Start")
score = 0
highscore = 0
invin = 0

def main():
    global score
    global speedx
    global speedy
    global addable
    global game_active
    global highscore
    global invin

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    paddles = pygame.sprite.Group()
    balls = pygame.sprite.Group()

    paddle = Paddle(board_image)
    paddles.add(paddle)
    all_sprites.add(paddle)

    ball = Ball(0, 0, 25, ball_image)
    balls.add(ball)
    all_sprites.add(ball)

    while True:
        for event in pygame.event.get():
            # If the close button is clicked, quit running
            if event.type == pygame.QUIT:
                sys.exit()

        invin += 1
                
        ballpaddlecollide = pygame.sprite.groupcollide(paddles, balls, False, False)
        if ballpaddlecollide:
            if invin > 35:
                if int(ball.rect.bottom) > paddle.rect.bottom:
                    speedx*=-1
                    invin = 0
                else:
                    speedy*=-1
                    score+=25
                    if score >= highscore:
                        highscore = score
                    addable = True
                    invin = 0

        if score > 0:
            if score%50 == 0:
                if addable == True:
                    if speedx > 0:
                        speedx+=0.5
                    else:
                        speedx-=0.5
                    if speedy > 0:
                        speedy+=0.5
                    else:
                        speedy-=0.5
                    addable = False

        if ball.rect.bottom > SCREEN_HEIGHT:
            game_active = False
            display_text(screen, "You lose!", 100, BLUE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        all_sprites.update()

        screen.fill(BLACK)
        all_sprites.draw(screen)

        if not game_active:
        # Display game over message
            display_text(screen, "Game Over", 50, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 180)
            display_text(screen, "You got " + str(score) + " points!", 30, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT // 2 - 100)
            if highscore == 0:
                display_text(screen, "High score: " + str(highscore) + " points???", 25, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT // 2 - 65)
            else:
                display_text(screen, "High score: " + str(highscore) + " points!", 25, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT // 2 - 65)
            startbutton("Play again")
            score = 0
            speedy = 6
            speedx = 6
            start()
        else:
            display_text(screen, "Score: " + str(score), 25, WHITE, 80, 20)
            display_text(screen, "High score: " + str(highscore), 25, WHITE, 80, 50)

        pygame.display.flip()

        clock.tick(34)

def start():
    global game_active
    while game_active == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if int(mouse_x) in range(int(SCREEN_WIDTH/2 - SCREEN_WIDTH/9), int(SCREEN_WIDTH/2 + SCREEN_WIDTH/9)):
                    if int(mouse_y) in range(int(SCREEN_HEIGHT/2 - SCREEN_HEIGHT/14), int(SCREEN_HEIGHT/2 + SCREEN_HEIGHT/14)):
                        game_active = True
                        screen.fill(BLACK)
                        main()

start()
    
