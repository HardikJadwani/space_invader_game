import pygame
import random
import math

from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")
#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 500
playerdX = 0

# enemies
enemyImg = []
enemyX = []
enemyY = []
enemydX = []
enemydY = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 200))
    enemydX.append(1)
    enemydY.append(20)

# bullet

# ready state: you cant see the bullet on the screen
# fire: the bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 500
bulletdX = 0
bulletdY = 3
bullet_state = 'ready'

distance = 0

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over font
g_over_font = pygame.font.Font('freesansbold.ttf', 64)
over_textX=200
over_textY=275

def show_score(x, y):
    score = font.render('Score :' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x,y):
    g_over_text = g_over_font.render('GAME OVER  :( ', True, (255, 255, 255))
    screen.blit(g_over_text,(x,y))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 22, y + 20))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    global distance
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is being pressed check whether its right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerdX = -2

            if event.key == pygame.K_RIGHT:
                playerdX = 2

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerdX = 0

    # checking for boundaries of spaceship so it does not go out of bounds
    playerX += playerdX
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # enemy movement
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i]>400:
            for j in range(num_of_enemies):
                enemyY[j]= 2000
            game_over_text(over_textX,over_textY)
            break
        enemyX[i] += enemydX[i]
        if enemyX[i] <= 0:
            enemydX[i] = 0.5
            enemyY[i] += enemydY[i]
        elif enemyX[i] >= 736:
            enemydX[i] = -0.5
            enemyY[i] += enemydY[i]

        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 500
            bullet_state = 'ready'
            score_value += 1

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 200)

        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletdY

        # print(distance)
    # elif(distance<50):
    # print(distance)

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
