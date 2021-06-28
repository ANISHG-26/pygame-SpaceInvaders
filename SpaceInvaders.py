import pygame
import random
import math

from pygame import mixer

# Initialize pygame

pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))

# Title and icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Background music
mixer.music.load('background.wav')
mixer.music.set_volume(0.1)
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(10)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Explosion
explosionImg = pygame.image.load('bomb.png')

# Score
score_value = 0
font = pygame.font.Font('Pacifico.ttf', 32)
text_X = 10
text_Y = 10

# Speed Factor

speedfactor = 4


# Display Score
def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


# Player functionality
def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy functionality
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Increase Enemy
def increase_enemies_speed(num_of_enemies,speedfactor):

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('alien.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(speedfactor)
        enemyY_change.append(10)

# Bullet Functionality

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision Functionality

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Explosion Effect
def explosion(x, y):
    screen.blit(explosionImg, (x, y))


# Collision Sound
def sound_generator():
    generate = random.randint(1, 6)
    if (generate == 1):
        collision_Sound = mixer.Sound('collision1.wav')

    elif (generate == 2):
        collision_Sound = mixer.Sound('collision2.wav')

    elif (generate == 3):
        collision_Sound = mixer.Sound('collision3.wav')

    elif (generate == 4):
        collision_Sound = mixer.Sound('collision4.wav')

    elif (generate == 5):
        collision_Sound = mixer.Sound('collision5.wav')

    else:
        collision_Sound = mixer.Sound('collision3.wav')
    collision_Sound.play()


# Game Over Message
over_font = pygame.font.Font('Pacifico.ttf', 100)


def game_over_text():
    bullet_state = "fire"
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (285, 250))


running = True

# Game loop
while running:

    # Screen Background
    screen.fill((0, 255, 200))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -5

            if event.key == pygame.K_d:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('pew.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    playerX += playerX_change

    # Display movement for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Display movement for enemy
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = speedfactor
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -speedfactor
            enemyY[i] += enemyY_change[i]

        # Collision Mechanic

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            sound_generator()
            explosionX = enemyX[i]
            explosionY = enemyY[i]
            explosion(explosionX, explosionY)
            bulletY = 480
            bullet_state = "ready"
            score_value += 5
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            num_of_enemies -= 1

            if num_of_enemies <= 4:
                num_of_enemies = 4
                if speedfactor <= 8:
                    speedfactor += 2
                    increase_enemies_speed(num_of_enemies,speedfactor)

        enemy(enemyX[i], enemyY[i], i)


    # Bullet Movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(text_X, text_Y)
    pygame.display.update()
