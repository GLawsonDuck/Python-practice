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
gravity = (80) #just throwing random numbers in here until the behaviour looks right, not sure how
#useful it would be to try to derive a number from pixel density etc.

#coefficient of restitution for collisions
ball_coeff = 0.712 #taken from a website, this is for a tennis ball

maxheight_unsupported = (screen.get_height() / 2) #need this for calculating accel during bounces/falls, initial maxheight is init player height

def fall_distance(dt):
    falldistance = ((gravity)*(dt ** 2))/2 # distance in m an object w/ constant acceleration falls in time t

    return falldistance

def fall_time(distance):
    falltime = math.sqrt((2 * distance)/gravity) #time it takes to fall a certain distance under constant acceleration

    return falltime

def instantaneous_yvelocity(yVelocity, time, bounced = False):
    instVelocity = yVelocity + (gravity * time)

    if bounced:
        pass #figure this out

    return instVelocity


def velocity_calc(init_velocity, **accels):
    accel = sum(accels)
    velocity = init_velocity + (accel * dt)
    return velocity

class Bounces:

    def __init__(self):
        self.num_bounces = 0
        self.yvelocity = 0

    def decay(self):
        self.yvelocity = -(self.yvelocity)*ball_coeff #the yvelocity needs to be the value from the previous frame

        if self.num_bounces > 10:
            bounced = False

bounce = 0
bounced = False

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) 

player_velocity = pygame.Vector2(x = 0, y = gravity * (dt ** 2))

player_accel = pygame.Vector2(x = 0, y = gravity)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    
    screen.fill("purple")
    pygame.draw.circle(screen, "red", player_pos, 40)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        #player_pos.y -= 300 * dt
        maxheight_unsupported = player_pos.y
        player_velocity.y -= 300 * dt
        player_accel.y -= 300

    if keys[pygame.K_s]:
        #player_pos.y += 300 * dt
        player_velocity.y += 300 * dt
        player_accel.y += 300

    if keys[pygame.K_a]:
        #player_pos.x -= 300 * dt
        player_velocity.x -= 300 * dt

    if keys[pygame.K_d]:
        #player_pos.x += 300 * dt
        player_velocity.x += 300 * dt

    if keys[pygame.K_SPACE] and not (keys[pygame.K_SPACE] * (clock.tick())):  #need to read documentation to extinguish jump effect after 1 button press, currently holding space keeps adding to y position
        #player_pos.y -= 500 * dt
        player_velocity.y -= 500 * dt

    if player_pos.x < border_left:
        player_pos.x = border_left
        bounced = True #do I even need this?
        player_velocity.x = -(player_velocity.x)*ball_coeff

    if player_pos.x > border_right:
        player_pos.x = border_right
        player_velocity.x = -(player_velocity.x)*ball_coeff

    if player_pos.y <= border_top:
        player_pos.y = border_top
        bounced = True
        player_velocity.y = -(player_velocity.y)*ball_coeff

    if player_pos.y >= border_bottom:
        player_pos.y = border_bottom
        bounced = True
        player_velocity.y = -(player_velocity.y)*ball_coeff

    player_accel.y += gravity

    player_pos.y += (gravity * dt) + player_velocity.y * dt
    player_pos.x += player_velocity.x * dt

    if player_pos.y > maxheight_unsupported: #record max height for bounce physics
        maxheight_unsupported = player_pos.y - 40
        print(maxheight_unsupported)

    if player_pos.y == 40: #this isn't going to work, but conceptually need a way to reset max height for following bounces or
        #if player controls are used, cancelling out bounce physics height. New maxheight should depend on "unsupported" height,
        #i.e. if player controls are used to move to a certain height and then the ball is released, release point will be new
        #value of maxheight.
        maxheight_unsupported = 0

        
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()