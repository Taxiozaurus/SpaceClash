__author__ = "Alexey Taxiozaurus Makeev"

#PREPARE TO DIE EDITION, (just kidding, though this will be a very hard game to get through)

import sys
import pygame
import random
import player
import projectile
import enemy
import powers

from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((600, 650))
pygame.display.set_caption('Space Clash')
frameRate = pygame.time.Clock()
##################################################################################################
# Global variables
green = (0, 255, 0)
black = (0, 0, 0)
d_grey = (80, 80, 80)
red = (255, 0, 0)
blue = (0, 0, 255)

explosion = pygame.image.load('assets/explosion.gif')
tutorial = pygame.image.load('assets/tutorial.png')
background = pygame.image.load('assets/background.png')
critical = pygame.image.load('assets/critical.png')

fontBig = pygame.font.Font('assets/font.ttf', 30)
fontSmall = pygame.font.Font('assets/font.ttf', 20)

difficulty = 15 # how many enemies are allowed to be on screen simultaneously also is used to get of how much speed is allowed for enemies by shoveling some random monkeys to run a marathon as well this will control your speed
mousex, mousey = 0, 0
click = False
frame = 0
speed = difficulty / 5
kills = 0
rounds = 1
wait = 250

# enemy data
countdown = rounds * 10
spawn_cooldown = 100
enemies = []
exploded = []
enemy_shot = []

# powers
power_ups = []

# player
user = player.Player(speed)
user_shot = []


def reset():
    global countdown, spawn_cooldown, kills, speed, enemies, power_ups, user_shot, exploded, enemy_shot
    countdown = rounds * 10
    spawn_cooldown = 100
    kills = 0
    speed = difficulty / 5
    enemies = []
    power_ups = []
    user_shot = []
    exploded = []
    enemy_shot = []
    user.speed = speed


def game_end():
    global frame
    reset()
    user.reset(True)
    frame = 0


def pickup_drop(x, y):
    chance = random.randint(0, 100)
    if chance > 99 and rounds % 3 == 0:
        power_ups.append(powers.Life(x, y))
    elif chance >= 90:
        power_ups.append(powers.Health(x, y))
    elif chance >= 60:
        power_ups.append(powers.Shield(x, y))


def spawn_enemy():
    global spawn_cooldown, countdown
    if len(enemies) < difficulty and countdown > 0:
        if spawn_cooldown > 0 :
            spawn_cooldown -= 1
        else :
            spawn_cooldown = 20
            if not countdown % 5 == 0:
                enemies.append(enemy.Enemy01(speed / 2))
            else :
                enemies.append(enemy.Enemy02(speed / 2))
            countdown -= 1


def overlay():

    base = pygame.Rect(0, 590, 600, 60)
    pygame.draw.rect(window, d_grey, base)

    txt = fontSmall.render("round: " + str(rounds), True, green, d_grey)
    trc = txt.get_rect()
    trc.topleft = (5, 600)
    window.blit(txt, trc)

    txt = fontSmall.render("kills: " + str(kills) + "/" + str(rounds * 10), True, green, d_grey)
    trc = txt.get_rect()
    trc.topleft = (5, 625)
    window.blit(txt, trc)

    txt = fontSmall.render("health: " + str(user.health), True, red, d_grey)
    trc = txt.get_rect()
    trc.topleft = (250, 615)
    window.blit(txt, trc)

    txt = fontSmall.render("shield: " + str(user.shield), True, blue, d_grey)
    trc = txt.get_rect()
    trc.topleft = (360, 615)
    window.blit(txt, trc)

    h = pygame.Rect(250, 605, user.health, 5)
    pygame.draw.rect(window, red, h)

    s = pygame.Rect(250, 599, user.shield, 5)
    pygame.draw.rect(window, blue, s)


def game():
    global frame, kills, wait
    rendered = user.render(mousex, mousey)
    if user.health > 0:

        if click :
            user_shot.append(projectile.Projectile(rendered[1].centerx, rendered[1].centery, mousex, mousey, speed * 2))

        for i in range(0, len(exploded)):
            if exploded[i].time > 0:
                window.blit(exploded[i].image, exploded[i].rect)
                exploded[i].time -= 1
        for i in range(len(exploded)-1, -1, -1):
            if exploded[i].time == 0:
                exploded.pop(i)

        window.blit(rendered[0], rendered[1])

        for i in range(len(user_shot)-1, -1, -1) :
            coord = user_shot[i].move()
            window.blit(coord[1], coord[0])
            enemy_hit = -1
            for a in range(0, len(enemies)) :
                if coord[0].colliderect(enemies[a].base):
                    enemy_hit = a
            if enemy_hit >= 0:
                user_shot.pop(i)
                enemies[enemy_hit].damage_taken(50)
            if not -50 < coord[0].centerx < 600 or not -50 < coord[0].centery < 600 :
                user_shot.pop(i)

        for i in range(len(enemies)-1, -1, -1) :
            if enemies[i].health > 0:
                coord = enemies[i].move(rendered[1].centerx, rendered[1].centery)
                window.blit(coord[0], coord[1])
                if enemies[i].name == "fighter":
                    if enemies[i].cooldown < 1:
                        enemies[i].cooldown = 20
                        enemy_shot.append(projectile.Projectile(coord[1].centerx, coord[1].centery, rendered[1].centerx, rendered[1].centery, speed * 1.5, red))
            else :
                exploded.append(powers.Placeholder(explosion, enemies[i].base))
                kills += 1
                pickup_drop(enemies[i].base.x, enemies[i].base.y)
                enemies.pop(i)

        for i in range(len(enemy_shot)-1, -1, -1):
            coord = enemy_shot[i].move()
            window.blit(coord[1], coord[0])
            if coord[0].colliderect(user.base):
                user.damage_taken(10)
                enemy_shot.pop(i)

        pressed = pygame.key.get_pressed()
        user.re_draw()
        if pressed[pygame.K_w] or pressed[pygame.K_UP]:
            user.move_up()
            user.re_draw(True)
        if pressed[pygame.K_a] or pressed[pygame.K_LEFT] :
            user.move_left()
            user.re_draw(True)
        if pressed[pygame.K_s] or pressed[pygame.K_DOWN] :
            user.move_down()
            user.re_draw(True)
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT] :
            user.move_right()
            user.re_draw(True)

        spawn_enemy()
        user.player_collision(power_ups, enemies)
        for i in range(len(power_ups)-1, -1, -1):
            window.blit(power_ups[i].surface, power_ups[i].base)
            if user.base.colliderect(power_ups[i].base):
                power_ups.pop(i)

        overlay()
        if kills >= rounds * 10:
            wait -= 1
        if kills >= rounds * 10 and wait < 1:
            frame = 2
            wait = 250
    elif user.lives > 0 :
        user.lives -= 1
        frame = 3
        user.reset()
        reset()
    else :
        game_end()
        print "game ended"


def menu():
    global frame, mousex, mousey
    play = fontBig.render("PLAY", True, black, green)
    base = play.get_rect()
    base.center = (500, 550)

    window.blit(play, base)
    if base.collidepoint(mousex, mousey) and click:
        frame = 1

    window.blit(tutorial, (0, 0))

while True:
    mousex, mousey = pygame.mouse.get_pos()
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    if user.health < 20:
        window.blit(critical, (0, 0))

    if frame == 0:
        menu()
    elif frame == 1:
        game()
    elif frame == 2:
        txt = fontSmall.render("level finished", True, green)
        trc = txt.get_rect()
        trc.center = (300, 250)
        window.blit(txt, trc)

        txt = fontBig.render("Continue", True, black, green)
        trc = txt.get_rect()
        trc.center = (300, 300)
        window.blit(txt, trc)

        if trc.collidepoint(mousex, mousey) and click:
            frame = 1
            rounds += 1
            if difficulty < 60:
                difficulty += 5
            reset()
    elif frame == 3: # you died sequence
        txt = fontSmall.render("You died, lives left: " + str(user.lives), True, red)
        trc = txt.get_rect()
        trc.center = (300, 250)
        window.blit(txt, trc)

        txt = fontBig.render("Continue", True, black, red)
        trc = txt.get_rect()
        trc.center = (300, 300)
        window.blit(txt, trc)

        if trc.collidepoint(mousex, mousey) and click:
            frame = 1
            if difficulty < 60:
                difficulty += 5
            reset()

    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN :
            click = True
        if event.type == MOUSEBUTTONUP :
            click = False

    pygame.display.update()
    frameRate.tick(60)