import pygame 
from constants import *
from ant import Ant
from snake import Snake 

pygame.init()
pygame.display.set_caption("ANT")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
play = False
play_button = pygame.image.load("assets/play.png")
hack_club = pygame.image.load("assets/hack_club.png")
back = pygame.image.load("assets/back.png")
ant_word = pygame.image.load("assets/ant.png")
ant_logo = pygame.image.load("assets/ant_logo.png")
credits = pygame.transform.scale(pygame.image.load("assets/credits.png"), (500, 50))

ant = Ant(col=5, row=5)

def draw_grid(surface):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            base_color = (255, 255, 255)
            pygame.draw.rect(surface, base_color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)


snake1 = Snake()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not play and play_button.get_rect(topleft=(200, 350)).collidepoint(event.pos):
                play = True
            elif play and back.get_rect(topleft=(10,10)).collidepoint(event.pos):
                play = False

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                ant.direction = "LEFT"
                ant.move(-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                ant.direction = "RIGHT"
                ant.move(1, 0)
            elif event.key in (pygame.K_UP, pygame.K_w):
                ant.direction = "UP"
                ant.move(0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                ant.direction = "DOWN"
                ant.move(0, 1)    

    if not play:
        screen.fill((0, 0, 0))
        screen.blit(ant_logo, (300, 70))
        screen.blit(play_button, (200, 350))
        screen.blit(hack_club, (100, 190))
        screen.blit(credits, (200, 530))
    
    else: 
        screen.fill((200, 200, 200))
        draw_grid(screen)
        ant.draw(screen)
        snake1.chase(ant)
        screen.blit(ant_word, (300, 100))
        screen.blit(back, (10, 10))
        snake1.draw(screen)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
