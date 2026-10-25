import pygame 
from constants import *
from ant import Ant
from snake import Snake 
from fruit import Fruit

pygame.init()
pygame.display.set_caption("ANT")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
play = False
dead = False
win = False
rules = False
fruit_counter = 0
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 74)
play_button = pygame.transform.scale(pygame.image.load("assets/menu/playbutton_unpressed.png"), (1000, 800))
play_button_hovered= pygame.transform.scale(pygame.image.load("assets/menu/playbutton_hovered.png"), (1000, 800))
hack_club = pygame.image.load("assets/hack_club.png")
back = pygame.image.load("assets/back.png")
ant_logo = pygame.image.load("assets/ant_logo.png")
credits = pygame.transform.scale(pygame.image.load("assets/credits.png"), (500, 150))
rules_button = pygame.image.load("assets/rules_button.png")
rules_background = pygame.image.load("assets/rules_background.png")
title_screen = pygame.transform.scale(pygame.image.load("assets/menu/titlescreen.png"), (1320, 770))

ant = Ant(col=5, row=5)
fruit = Fruit()

def draw_grid(surface):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            base_color = (255, 255, 255)
            pygame.draw.rect(surface, base_color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)


snake1 = Snake()
while running:
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not play and play_button.get_rect(topleft=(450, 450)).collidepoint(event.pos):
                play = True
                snake1.reset(0, 0)
                ant.col = 5
                ant.row = 5
                fruit.respawn(snake1.body, (ant.col, ant.row))
                fruit_counter = 0

            elif play and back.get_rect(topleft=(10,10)).collidepoint(event.pos) or dead and back.get_rect(topleft=(10,10)).collidepoint(event.pos) or win and back.get_rect(topleft=(10,10)).collidepoint(event.pos):
                play = False
                dead = False
                rules = False
                win = False
                snake1.reset(0, 0)
                ant.col = 5
                ant.row = 5

            elif not play and rules_button.get_rect(topleft=(460,350)).collidepoint(event.pos):
                rules = True

    if not play and not dead and not win and not rules:
        # Main Menu
        screen.blit(title_screen, (0, 0))
        if play_button.get_bounding_rect().move(200,100).collidepoint(pygame.mouse.get_pos()) or play_button_hovered.get_bounding_rect().move(200,100).collidepoint(pygame.mouse.get_pos()):
            screen.blit(play_button_hovered, (200, 100))
        else:
            screen.blit(play_button, (200, 100))
    
    elif not dead and not win and not rules: 
        # Game
        screen.fill((200, 200, 200))
        draw_grid(screen)
        ant.handle_held_movement()
        ant.update_animation()
        ant.draw(screen, fruit_counter)
        snake1.chase(ant)
        if ant.col == fruit.col and ant.row == fruit.row:
            fruit.respawn(snake1.body, (ant.col, ant.row))
            fruit_counter +=1
        screen.blit(back, (10, 10))
        fruit.draw(screen)
        fruit_score_surface = font.render(f"Fruit Counter: {fruit_counter}", True, (0,0,0))
        fruit_score_rect = fruit_score_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(fruit_score_surface, fruit_score_rect)
        snake1.draw(screen)

    elif not play and not win and not rules:
        # Death screen
        screen.fill((0, 0, 0))
        text = large_font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        screen.blit(back, (10, 10))

    elif not play and not dead and not rules:
        # Victory screen
        screen.fill((222, 221, 150))
        text = large_font.render("Victory!", True, (222, 175, 145))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
        screen.blit(text, text_rect)
        screen.blit(back, ((10,10)))

    else:
        # Rules screen
        screen.blit(rules_background, (0,0))
        screen.blit(back, ((10,10)))

    if ant.col == snake1.col and ant.row == snake1.row:
        if fruit_counter >= 10:
            win = True
            play = False
        else:
            play = False
            dead = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
