import pygame 
import random
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

current_level = 1
levels = {
    1: {
        "ant_step_delay": 200,
        "snake_step_delay": 400,
        "required_fruit": 5,
    },
    2: {
        "ant_step_delay": 225,
        "snake_step_delay": 375,
        "required_fruit": 7
    },
    3: {
        "ant_step_delay": 250,
        "snake_step_delay": 350,
        "required_fruit": 9
    },
    4: {
        "ant_step_delay": 275,
        "snake_step_delay": 325,
        "required_fruit": 11
    },
    5: {
        "ant_step_delay": 300,
        "snake_step_delay": 300,
        "required_fruit": 13
    },
    6: {
        "ant_step_delay": 325,
        "snake_step_delay": 275,
        "required_fruit": 15
    }
}

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
snake1 = Snake()
fruit = Fruit(fruit_type = "banana")

def respawn_fruit(snake, ant):
    global fruit
    random_no = random.randint(0, 5)
    if random_no == 0:
        fruit.set_type("apple")
    else:
        fruit.set_type("banana")
    fruit.respawn(snake.body, (ant.col, ant.row))

def draw_fruit(screen):
    fruit.draw(screen)

def draw_grid(surface):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            base_color = (255, 255, 255)
            pygame.draw.rect(surface, base_color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)

def load_level(level_no):
    global fruit_counter
    level_settings = levels[level_no]

    ant.step_delay = level_settings["ant_step_delay"]
    snake1.move_delay = level_settings["snake_step_delay"]

    ant.col = 5
    ant.row = 5
    snake1.reset(0,0)
    respawn_fruit(snake1, ant)
    fruit_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not play and play_button.get_rect(topleft=(450, 450)).collidepoint(event.pos):
                current_level = 1
                load_level(current_level)
                play = True
                dead = False
                win = False
                rules = False

            elif (play or dead or win or rules) and back.get_rect(topleft=(10, 10)).collidepoint(event.pos):
                play = False
                dead = False
                rules = False
                win = False
                current_level = 1
                snake1.reset(0, 0)
                ant.col = 5
                ant.row = 5

            elif not play and rules_button.get_rect(topleft=(460,350)).collidepoint(event.pos):
                rules = True

    if not play and not dead and not win and not rules:
        # Main Menu
        screen.blit(title_screen, (0, 0))
        if play_button.get_bounding_rect().move(200,100).collidepoint(pygame.mouse.get_pos()) or \
            play_button_hovered.get_bounding_rect().move(200,100).collidepoint(pygame.mouse.get_pos()):
            screen.blit(play_button_hovered, (200, 100))
        else:
            screen.blit(play_button, (200, 100))
    
    elif play and not dead and not win and not rules: 
        # Game
        screen.fill((200, 200, 200))
        draw_grid(screen)

        ant.update_power_ups()
        ant.handle_movement(snake1)
        ant.update_animation()
        ant.draw(screen, fruit_counter)
        snake1.chase(ant)

        # Check if fruit has been eaten
        if ant.col == fruit.col and ant.row == fruit.row:
            if fruit.fruit_type == "apple":
                # Enable power up (increase ant speed for 5 seconds)
                ant.enable_speed_up()
            respawn_fruit(snake1, ant)
            fruit_counter += 1

            # Check if level has been completed
            if fruit_counter >= levels[current_level]["required_fruit"]:
                if current_level in levels and (current_level + 1) in levels:
                    current_level += 1
                    load_level(current_level)
                else:
                    win = True
                    play = False

        if ant.col == snake1.col and ant.row == snake1.row:
            dead = True
            play = False
            
        screen.blit(back, (10, 10))
        draw_fruit(screen)
        snake1.draw(screen)

        fruit_score_surface = font.render(f"Fruit Counter: {fruit_counter}/{levels[current_level]['required_fruit']}", True, (0,0,0))
        fruit_score_rect = fruit_score_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(fruit_score_surface, fruit_score_rect)
        level_counter_surface = font.render(f"Level: {current_level}", True, (0,0,0))
        level_counter_rect = level_counter_surface.get_rect(topright=(SCREEN_WIDTH - 20, 50))
        screen.blit(level_counter_surface, level_counter_rect)

    elif dead:
        # Death screen
        screen.fill((0, 0, 0))
        text = large_font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        level_text = font.render(f"You completed {current_level-1} level{"s" if current_level-1 != 1 else ""}.", True, (255, 0, 0))
        text_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(level_text, text_rect)
        screen.blit(back, (10, 10))

    elif win:
        # Victory screen
        screen.fill((222, 221, 150))
        text = large_font.render("Victory!", True, (222, 175, 145))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
        screen.blit(text, text_rect)
        screen.blit(back, ((10,10)))

    elif rules:
        # Rules screen
        screen.blit(rules_background, (0,0))
        screen.blit(back, ((10,10)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
