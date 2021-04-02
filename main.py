import pygame
import os
pygame.font.init()

FPS = 60
VEL = 5
BULLET_VEL = 7

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 45, 30

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (190, 200, 141)

BORDER = pygame.Rect(347, 0, 6, SCREEN_HEIGHT)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SPACE FIGHT!")

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'yellowSpaceship.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'redSpaceship.png'))

YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("HEALTH: "+str(red_health), 1, BLACK)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, BLACK)
    screen.blit(red_health_text, (SCREEN_WIDTH-red_health_text.get_width(), 10))
    screen.blit(yellow_health_text, (10, 10))

    screen.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    screen.blit(RED_SPACESHIP, (red.x, red.y))


    for bullet in red_bullets:
        pygame.draw.rect(screen, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL >0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL >0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height <SCREEN_HEIGHT:
        yellow.y += VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < SCREEN_WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL >0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < SCREEN_HEIGHT:
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > SCREEN_WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLUE)
    screen.blit(draw_text, (SCREEN_WIDTH//2 - draw_text.get_width()//2, SCREEN_HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(600, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health =10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
            if event.type == RED_HIT:
                red_health -=1
            if event.type == YELLOW_HIT:
                yellow_health -=1
        winner_text =''

        if red_health <= 0:
            winner_text = 'YELLOW WINS'

        if yellow_health <= 0:
            winner_text = 'RED WINS'

        if winner_text != '':
            draw_winner(winner_text)
            break


        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
    pygame.quit()

if __name__ == "__main__":
    main()