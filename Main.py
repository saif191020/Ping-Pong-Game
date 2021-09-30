import pygame
import random
import sys


def ball_movement():
    global ball_speed_y, ball_speed_x, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        pygame.mixer.Sound.play(score_sound)
        ball_speed_x, ball_speed_y = 0, 0
        score_time = pygame.time.get_ticks()
        ball_restart()
    if ball.colliderect(player) or ball.colliderect(opponent):
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_x *= -1
        ball.x += ball_speed_x
        ball.y += ball_speed_y


def ball_restart():
    global ball_speed_y, ball_speed_x, player_score, opponent_score
    if ball.left <= 0:
        opponent_score += 1
    elif ball.right >= SCREEN_WIDTH:
        player_score += 1
    ball.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])


def player_movement():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def opponent_movement():
    opponent_speed = 7
    if opponent.top >= ball.y:
        opponent.top -= opponent_speed
    elif opponent.bottom <= ball.y:
        opponent.top += opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT


# General Setup
# pygame.mixer.pre_init(4410,-16,2,512) default
pygame.init()
clock = pygame.time.Clock()

# Screen Setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('pong')


# Game Rectangle
ball = pygame.Rect(SCREEN_WIDTH/2 - 15, SCREEN_HEIGHT/2-15, 30, 30)
player = pygame.Rect(10, SCREEN_HEIGHT/2-70, 10, 140)
opponent = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT/2-70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
text_grey = (77, 77, 77)


ball_speed_x = 7
ball_speed_y = 7

# Text Setup
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 300)
game_time_font = pygame.font.Font("freesansbold.ttf", 48)


# Timer
score_time = None

# Sounds
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
player_speed = 0
# Game Loop
while True:
    # Event Handeling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # visuals
    ball_movement()
    player_movement()
    opponent_movement()

    screen.fill(bg_color)

    if score_time:
        secs = pygame.time.get_ticks()-score_time
        if secs < 700:
            number_3 = game_time_font.render("3", False, pygame.Color('red'))
            screen.blit(number_3, (SCREEN_WIDTH/2-10, SCREEN_HEIGHT/2+20))
        if secs >= 700 and secs < 1700:
            number_2 = game_time_font.render("2", False, pygame.Color('red'))
            screen.blit(number_2, (SCREEN_WIDTH/2-10, SCREEN_HEIGHT/2+20))

        if secs >= 1700 and secs < 2700:
            number_1 = game_time_font.render("1", False, pygame.Color('red'))
            screen.blit(number_1, (SCREEN_WIDTH/2-10, SCREEN_HEIGHT/2+20))

        if(secs >= 2700):
            ball_speed_x, ball_speed_y = 7, 7
            score_time = None
            ball_restart()
        else:
            pass

    player_score_text = game_font.render(f'{player_score}', False, text_grey)
    opponent_score_text = game_font.render(
        f'{opponent_score}', False, text_grey)
    screen.blit(player_score_text, (SCREEN_WIDTH/4, 200))
    screen.blit(opponent_score_text, ((SCREEN_WIDTH/4)*2+150, 200))

    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH/2, 0),
                       (SCREEN_WIDTH/2, SCREEN_HEIGHT))

    # Update Window
    pygame.display.flip()
    clock.tick(60)
