# Pong Desktop Attempt

import pygame
import sys
import math
import random

pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((400, 700))
GAME_FONT = pygame.font.SysFont("Arial", 24)


border_left, border_right, border_bottom, border_top = [10, (screen.get_width() - 10), (screen.get_height() - 10), 10]

#Clock stuff
clock = pygame.time.Clock()
running = True
dt = 0

paddlewidth = 60
paddlethickness = 15
ballradius = 8

class Player:

    def __init__(self, ypos):
        self.score = 0
        self.pos = pygame.Vector2(x = screen.get_width()/2, y = ypos)
        self.paddle = pygame.Rect((self.pos.x - (paddlewidth/2)), (self.pos.y), paddlewidth, paddlethickness)


class Ball:

    def __init__(self):
        self.pos = pygame.Vector2(x = screen.get_width()/2, y = screen.get_height()/2)
        self.velocity = pygame.Vector2(x = 0, y = -10)


player1 = Player(border_bottom - 20)
computer = Player(border_top + 30)
ball = Ball()

bouncer = pygame.mixer.Sound('bounce.wav')

player_wins = 0
computer_wins = 0

running = True
state = 'Playing'
level = 0
paddlejiggle = 0

#Levels:

level1 = pygame.Rect(screen.get_width()/2 - 75, screen.get_height()/2, 150, 20)

level21 = pygame.Rect(screen.get_width()/2 - 145, screen.get_height()/2 - 100, 20, 200)
level22 = pygame.Rect(screen.get_width()/2 + 125, screen.get_height()/2 - 100, 20, 200)


while running:

    while state == 'Playing':

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = 'Endgame'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = 'Paused'

        pygame.mouse.set_visible(False)

        paddlejiggle = random.randint(-3, 3)
        computer.paddle.centerx += paddlejiggle   

        screen.fill('black')

        scorecard = GAME_FONT.render(('Player Wins: ' + str(player_wins) + ' Computer Wins: ' + str(computer_wins)), True, ('white'))
        screen.blit(scorecard, (0, 0))

        if border_left > ball.pos.x or border_right < ball.pos.x:
            pygame.mixer.Sound.play(bouncer)
            ball.velocity.x *= -1
        
        if player1.paddle.collidepoint(ball.pos):
            pygame.mixer.Sound.play(bouncer)
            ball.pos.y = (player1.paddle.top - 1)
            ball.velocity.y *= -1
            if player1.paddle.centerx - (screen.get_width()/2) > 0:
                ball.velocity.x += 3
            elif player1.paddle.centerx - (screen.get_width()/2)  < 0:
                ball.velocity.x -= 3     
        
        if computer.paddle.collidepoint(ball.pos):
            pygame.mixer.Sound.play(bouncer)
            ball.pos.y = (computer.paddle.bottom + 1)
            ball.velocity.y *= -1
            if computer.paddle.centerx - (screen.get_width()/2) > 0:
                ball.velocity.x += 3
            elif computer.paddle.centerx - (screen.get_width()/2)  < 0:
                ball.velocity.x -= 3            
            

        if ball.pos.x > computer.paddle.centerx:
            if ball.pos.x - computer.paddle.centerx > 100:
                computer.paddle.move_ip(9, 0)
            elif ball.pos.x - computer.paddle.centerx > 50:
                computer.paddle.move_ip(7, 0)
            elif ball.pos.x - computer.paddle.centerx > 20:
                computer.paddle.move_ip(5, 0)
            elif ball.pos.x - computer.paddle.centerx > 5:
                computer.paddle.move_ip(1, 0)
        
        if ball.pos.x < computer.paddle.centerx:
            if computer.paddle.centerx - ball.pos.x > 100:
                computer.paddle.move_ip(-9, 0)
            elif computer.paddle.centerx - ball.pos.x > 50:
                computer.paddle.move_ip(-7, 0)
            elif computer.paddle.centerx - ball.pos.x > 20:
                computer.paddle.move_ip(-5, 0)
            elif computer.paddle.centerx - ball.pos.x > 5:
                computer.paddle.move_ip(-1, 0)

        if ball.pos.y > border_bottom + 10:
            ball.velocity.y = 1

            if ball.pos.y > border_bottom + 40:
                ball.pos.y = screen.get_height()/2
                ball.pos.x = screen.get_width()/2
                ball.velocity.y = -10
                ball.velocity.x = round(ball.velocity.x/10)
                computer_wins += 1
                if level ==0 and computer_wins >= 3 and computer_wins < 5:
                    level = 1
                    ball.velocity.y -= 1
                if level == 1 and (computer_wins >= 5 and computer_wins < 7):
                    level = 2
                    ball.velocity.y -= 2

                if computer_wins == 10:
                    state = 'Endgame'

        if ball.pos.y < border_top - 10:
            ball.velocity.y = -1

            if ball.pos.y < border_top - 40:
                ball.pos.y = screen.get_height()/2
                ball.pos.x = screen.get_width()/2
                ball.velocity.y = 10
                ball.velocity.x = round(ball.velocity.x/10)
                player_wins += 1
                if level == 0 and player_wins >= 3 and player_wins < 5:
                    level = 1
                    ball.velocity.y += 1
                if level == 1 and (player_wins >= 5 and player_wins < 7):
                    level = 2
                    ball.velocity.y += 2

                if player_wins == 10:
                    state = 'Endgame'
        
        player1.paddle.x = pygame.mouse.get_pos()[0]

        pygame.draw.circle(screen, 'white', ball.pos, ballradius)
        pygame.draw.rect(screen, 'white', player1.paddle)
        pygame.draw.rect(screen, 'white', computer.paddle)

        if level == 1:
            pygame.draw.rect(screen, 'white', level1)
            if level1.collidepoint(ball.pos):
                if ball.pos.y < level1.centery and ball.pos.x > level1.left and ball.pos.x < level1.right:
                    pygame.mixer.Sound.play(bouncer)
                    ball.pos.y = level1.top - 1
                    ball.velocity.y = -(ball.velocity.y)
                if ball.pos.y > level1.centery and ball.pos.x > level1.left and ball.pos.x < level1.right:
                    pygame.mixer.Sound.play(bouncer)
                    ball.pos.y = level1.bottom + 1
                    ball.velocity.y = -(ball.velocity.y)
                if (ball.pos.x == level1.left - ballradius) or (ball.pos.x == level1.right + ballradius):
                    pygame.mixer.Sound.play(bouncer)
                    ball.velocity.x = -(ball.velocity.x)

        if level == 2:
            pygame.draw.rect(screen, 'white', level21)
            pygame.draw.rect(screen, 'white', level22)
            if level21.collidepoint(ball.pos):
                if ball.pos.y < level21.centery - 99 and ball.pos.x > level21.left and ball.pos.x < level21.right:
                    pygame.mixer.Sound.play(bouncer)
                    ball.pos.y = level21.top - 1
                    ball.velocity.y = -(ball.velocity.y)
                if ball.pos.y > level21.centery + 99 and ball.pos.x > level21.left and ball.pos.x < level21.right:
                    pygame.mixer.Sound.play(bouncer)
                    ball.pos.y = level21.bottom + 1
                    ball.velocity.y = -(ball.velocity.y)
                if ball.pos.y > level21.top and ball.pos.y < level21.bottom:
                    pygame.mixer.Sound.play(bouncer)
                    ball.velocity.x = -(ball.velocity.x)

            if level22.collidepoint(ball.pos):
                if ball.pos.y < level22.centery - 99 and ball.pos.x > level22.left and ball.pos.x < level22.right:
                    pygame.mixer.Sound.play(bouncer)
                    ball.pos.y = level22.top - 1
                    ball.velocity.y = -(ball.velocity.y)
                if ball.pos.y > level22.centery + 99 and ball.pos.x > level22.left and ball.pos.x < level22.right:
                    pygame.mixer.Sound.play(bouncer)
                    ball.pos.y = level22.bottom + 1
                    ball.velocity.y = -(ball.velocity.y)
                if ball.pos.y > level22.top and ball.pos.y < level22.bottom:
                    pygame.mixer.Sound.play(bouncer)
                    ball.velocity.x = -(ball.velocity.x)                                


        
        ball.pos.x += ball.velocity.x
        ball.pos.y += ball.velocity.y

        pygame.display.flip()

        dt = clock.tick(60) / 1000


    while state == 'Paused':

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = 'Endgame'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = 'Playing'


        screen.fill('white') #invert colors

        textheight = screen.get_height()/2
        if level == 1:
            textheight -= 80
        if level == 2:
            textheight += 150


        scorecard = GAME_FONT.render(('Player Wins: ' + str(player_wins) + ' Computer Wins: ' + str(computer_wins)), True, ('black'))
        screen.blit(scorecard, (55, textheight))

        pausetext = GAME_FONT.render(('Game Paused'), True, ('black'))
        screen.blit(pausetext, (55, textheight + 20))

        pygame.draw.rect(screen, 'black', player1.paddle)
        pygame.draw.rect(screen, 'black', computer.paddle)
        pygame.draw.circle(screen, 'black', ball.pos, 8)

        if level == 1:
            pygame.draw.rect(screen, 'black', level1)

        if level == 2:
            pygame.draw.rect(screen, 'black', level21)
            pygame.draw.rect(screen, 'black', level22)


        pygame.display.flip()


    while state == 'Endgame':

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.fill('black')

        keys = pygame.key.get_pressed()

        winner = ''

        if player_wins == 10 or computer_wins == 10:

            if player_wins > computer_wins:
                winner = 'You beat the computer!'
            elif computer_wins > player_wins:
                winner = 'You lost to the computer :('

        if winner:

            scorecard = GAME_FONT.render(('Player Wins: ' + str(player_wins) + ' Computer Wins: ' + str(computer_wins)), True, ('white'))
            screen.blit(scorecard, (50, screen.get_height()/4))

            wintext = GAME_FONT.render(winner, True, ('white'))
            screen.blit(wintext, (100, (screen.get_height()/2)))

            playagain = GAME_FONT.render('Play again? Y/N', True, ('white'))
            screen.blit(playagain, (130, (screen.get_height()/2) + 80))

            if keys[pygame.K_y]:
                level = 0
                player_wins = 0
                computer_wins = 0
                state = 'Playing'

            if keys[pygame.K_n]:
                pygame.quit()

        elif not winner:

            scorecard = GAME_FONT.render(('Player Wins: ' + str(player_wins) + ' Computer Wins: ' + str(computer_wins)), True, ('white'))
            screen.blit(scorecard, (50, screen.get_height()/2))

            continuegame = GAME_FONT.render(('Continue playing? Y/N'), True, 'white')
            screen.blit(continuegame, (100, screen.get_height()/2 + 60))

            if keys[pygame.K_y]:
                state = 'Playing'
                
            if keys[pygame.K_n]:
                pygame.quit()

        
        pygame.display.flip()


pygame.quit()


