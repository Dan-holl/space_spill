import math
import random
import pygame
from pygame import mixer
pygame.mixer.init()

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("song.mp3")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('fighter-jet.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('jet-plane.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)  # Make enemies move slower
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Missile
missileImg = pygame.transform.scale(pygame.image.load('missile.png'), (32, 32))
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 2
missile_state = "ready"

# Explosion
explosionImg = pygame.image.load('explode.png')
explosion_states = ["ready"] * num_of_enemies
explosion_positions = [(0, 0)] * num_of_enemies  # Track explosion positions
explosion_start_time = [0] * num_of_enemies

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_m:
                if missile_state == "ready":
                    missileSound = mixer.Sound("laser.wav")
                    missileSound.play()
                    missileX = playerX + (playerImg.get_width() // 2) - (missileImg.get_width() // 2)
                    fire_missile(missileX, missileY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                explosion_states[j] = "ready"
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2  # Make enemies move slower
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2  # Make enemies move slower
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            explosion_states[i] = "explode"
            explosion_positions[i] = (enemyX[i], enemyY[i])  # Store explosion position
            explosion_start_time[i] = pygame.time.get_ticks()
            # Respawn the enemy
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            missileY = 480
            missile_state = "ready"
            score_value += 1
            explosion_states[i] = "explode"
            explosion_positions[i] = (enemyX[i], enemyY[i])  # Store explosion position
            explosion_start_time[i] = pygame.time.get_ticks()
            # Respawn the enemy
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change

    player(playerX, playerY)
    show_score(textX, testY)

    for i in range(num_of_enemies):
        if explosion_states[i] == "explode":
            current_time = pygame.time.get_ticks()
            if current_time - explosion_start_time[i] >= 500:  # 2 seconds in milliseconds
                explosion_states[i] = "ready"

        if explosion_states[i] == "explode":
            screen.blit(explosionImg,
                        (explosion_positions[i][0] + (enemyImg[i].get_width() // 2) - (explosionImg.get_width() // 2),
                         explosion_positions[i][1] + (enemyImg[i].get_height() // 2) - (explosionImg.get_height() // 2)))

    pygame.display.update()