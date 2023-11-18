# Example file showing a circle moving on screen
import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

borders = [40, (screen.get_width() - 40), screen.get_height() - 40, 40]

border_left, border_right, border_bottom, border_top = borders


clock = pygame.time.Clock()
running = True
dt = 0

#initial y velocity comes from gravity, y axis is flipped
gravity = (9.8) * ((720/16.1)) #9.8 m/s * 720 pixels divided by 16.1mm (measured on my screen)
#currently this value is not interacting with the other values I randomly threw in very well, 
#so I am using 16.1 rather than the 0.0161 the 16.1mm value should be in future
yvelocity = gravity

#coefficient of restitution for collisions
ball_coeff = 0.92
surface_coeff = 0.98

maxheight = 40 #need this for calculating accel during bounces/falls

class Bounces:

    def __init__(self):
        self.num_bounces = 0
        self.yvelocity = -(yvelocity)*ball_coeff*surface_coeff

    def decay(self):


        if self.num_bounces > 10:
            bounced = False

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

    player_pos.y += (gravity * dt)

    if bounced == True:
        player_pos.y += 15 * (bounce * dt)
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
    if keys[pygame.K_SPACE] and not (keys[pygame.K_SPACE] * (clock.tick())):  #need to read documentation to extinguish jump effect after 1 button press, currently holding space keeps adding to y position
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

    if player_pos.y > maxheight: #record max height for bounce physics
        maxheight = player_pos.y
        print(maxheight)

    if player_pos.y == 40: #this isn't going to work, but conceptually need a way to reset max height for following bounces or
        #if player controls are used, cancelling out bounce physics height. New maxheight should depend on "unsupported" height,
        #i.e. if player controls are used to move to a certain height and then the ball is released, release point will be new
        #value of maxheight.
        maxheight = 0

        
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()