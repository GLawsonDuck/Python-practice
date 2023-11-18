# Example file showing a circle moving on screen
import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

borders = [40, (screen.get_width() - 40), screen.get_height() - 40, 40]
border_left = borders[0]
border_right = borders[1]
border_bottom = borders[2]
border_top = borders[3]


clock = pygame.time.Clock()
running = True
dt = 0

class Bounces:

    def __init__(self):
        self.num_bounces = 0




bounce = 0
bounced = False

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    gravity = 200

    player_pos.y += (gravity * dt)

    if bounced == True:
        player_pos.y += 15 * (bounce * dt)
        print(bounce)
        bounce += 60

        if bounce >= 0:
            bounced = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    if keys[pygame.K_SPACE]:
        player_pos.y -= 500 * dt

    if player_pos.x < border_left:
        player_pos.x = border_left
    if player_pos.x > border_right:
        player_pos.x = border_right
    if player_pos.y < border_top:
        player_pos.y = border_top
    if player_pos.y >= border_bottom:
        player_pos.y -= 600 * dt
        bounced = True
        bounce = -300


        
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()