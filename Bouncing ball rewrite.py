import pygame
import random
import math

#Pygame setup:

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
GAME_FONT = pygame.freetype.Font("C:\Windows\Fonts\Arial.ttf", 24)

border_left, border_right, border_bottom, border_top = [40, (screen.get_width() - 40), (screen.get_height() - 40), 40]

#Clock stuff
clock = pygame.time.Clock()
running = True
dt = 0

# gravity
gravity = 0.98

#User setup
class Ball:

    def __init__(self):
        self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.pos_initial = self.pos

        self.velocity = pygame.Vector2(0, 0)
        self.velocity_initial = self.velocity

        self.acceleration = pygame.Vector2(0, gravity)

        self.coeff = 0.72 #coefficient of restitution for collisions

        self.unsup_height = (border_bottom - self.pos.y)
        self.unsup_time = pygame.time.get_ticks()
        self.unsup_duration = 0

    def collidepoint():
        pass


# other basics
ball = Ball()
jumped = False
coins = []
coincircles = []
coincount = 0
bottom = False

coiner = pygame.mixer.Sound('coins.wav')
bouncer = pygame.mixer.Sound('bounce.wav')

wobbler = 1

while len(coins) < 10:
    x = len(coins)
    randomx = random.randint(border_left, border_right)
    randomy = random.randint(border_top, border_bottom)
    coinvect = pygame.Vector2(randomx, randomy)
    coins.append(coinvect)


#Game loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                jumped = False


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    #draw in coins and player
    for x in range(len(coins)):
        pygame.draw.circle(screen,(150, 250, 000), coins[x], 10)

    # collisions and wobble
    for coinpos in coins:
        if int(coinpos[0]) in range(int(ball.pos.x) - 30, int(ball.pos.x) + 30) and int(coinpos[1]) in range(int(ball.pos.y) - 30, int(ball.pos.y) + 30):
            coincircles.append([coinpos[0],coinpos[1], 10, 20]) # x, y, initial radius, repetitions
            pygame.mixer.Sound.play(coiner)
            coins.remove(coinpos)
            randomx = random.randint(border_left, border_right)
            randomy = random.randint(border_top, border_bottom)
            coinvect = pygame.Vector2(randomx, randomy)
            coins.append(coinvect)

        wobble = math.sin(wobbler)
        coinpos[1] += wobble
        wobbler += 0.01    

    # pop circles
    for coincircle in coincircles:
        if coincircle[3] == 0:
            coincircles.remove(coincircle)
        
        else:
            pygame.draw.circle(screen, color = "yellow", center = (coincircle[0], coincircle[1]), radius = coincircle[2], width = round(coincircle[3]/1.1))
            coincircle[2] += 2 #radius increase
            coincircle[3] -= 1 #repetitions left



    pygame.draw.circle(screen, "red", ball.pos, 40)

    ball.pos_initial = ball.pos
    ball.velocity_initial = ball.velocity

    # gravity
    if ball.pos.y < (border_bottom):
        ball.velocity.y += gravity

    # check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        ball.pos.y -= 10
        ball.velocity.y -= 5
        bottom = False
        if (border_bottom - ball.pos.y) > 0:
            ball.unsup_height = (border_bottom - ball.pos.y)
        else:
            ball.unsup_height = 0
        ball.unsup_time = pygame.time.get_ticks()


    if keys[pygame.K_s]:
        ball.pos.y += 10
        ball.velocity.y += 5
        if (border_bottom - ball.pos.y) > 0:
            ball.unsup_height = (border_bottom - ball.pos.y)
        else:
            ball.unsup_height = 0
            bottom = True
        ball.unsup_time = pygame.time.get_ticks()  

    if keys[pygame.K_a]:
        ball.pos.x -= 10
        ball.velocity.x -= 5

    if keys[pygame.K_d]:
        ball.pos.x += 10
        ball.velocity.x += 5

    if keys[pygame.K_SPACE] and jumped == False:
        ball.pos.y -= 5
        ball.velocity.y -= 10
        bottom = False
        if (border_bottom - ball.pos.y) > 0:
            ball.unsup_height = (border_bottom - ball.pos.y)
        else:
            ball.unsup_height = 0
        ball.unsup_time = pygame.time.get_ticks()
        jumped = True
    
    # keeping track of unsupported fall
    ball.unsup_duration = pygame.time.get_ticks() - ball.unsup_time

    # momentum
    if border_bottom > ball.pos.y and border_top < ball.pos.y:
        ball.pos.y += ball.velocity.y #ball has momentum inside user view

    if border_left < ball.pos.x and border_right > ball.pos.x:
        ball.pos.x += ball.velocity.x


    # bounce
    if border_bottom <= ball.pos.y:
        ball.pos.y = border_bottom - 1
        ball.velocity.y = -(ball.velocity.y) * ball.coeff
        if ball.unsup_height > 0.9:
            pygame.mixer.Sound.play(bouncer)
            print(ball.unsup_height)

    if border_top >= ball.pos.y:
        ball.pos.y = border_top + 1
        ball.velocity.y = -(ball.velocity.y) * ball.coeff
        pygame.mixer.Sound.play(bouncer)

    if border_left >= ball.pos.x:
        ball.pos.x = border_left + 1
        ball.velocity.x = -(ball.velocity.x) * (ball.coeff + 0.1)
        pygame.mixer.Sound.play(bouncer)

    if border_right <= ball.pos.x:
        ball.pos.x = border_right - 1
        ball.velocity.x = -(ball.velocity.x) * (ball.coeff + 0.1)
        pygame.mixer.Sound.play(bouncer)

    # rolling friction:
    if ball.pos.y == (border_bottom -1) and ball.velocity.x != 0:
        x_abs = abs(ball.velocity.x)
        sign = (x_abs/ball.velocity.x)
        ball.velocity.x = (x_abs * 0.98 * sign)


    #GAME_FONT.render_to(screen, (ball.pos.x - 20, ball.pos.y - 20), ("Vx =" + str(round(ball.velocity.x)) ), (0, 0, 0))
    #GAME_FONT.render_to(screen, (ball.pos.x - 20, ball.pos.y), ("Vy = " + str(round(ball.velocity.y))), (0, 0, 0))
    #GAME_FONT.render_to(screen, (ball.pos.x - 20, ball.pos.y + 20), ("unsup height = " + str(round(ball.unsup_height))), (0, 0, 0))

    #tracking unsupported height (last height assumed to be unsupported during loop unless overwritten by keypress)
    if (border_bottom - ball.pos.y) < ball.unsup_height and not (border_bottom - ball.pos.y) < 0.9: 
        ball.unsup_height = (border_bottom - ball.pos.y)
    elif (border_bottom - ball.pos.y) < ball.unsup_height and (border_bottom - ball.pos.y) < 0.9:
        ball.unsup_height = 0
        bottom = True

    if bottom:
        print("bottom")

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()