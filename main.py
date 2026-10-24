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
dead = False
play_button = pygame.image.load("assets/play.png")
hack_club = pygame.image.load("assets/hack_club.png")
back = pygame.image.load("assets/back.png")
ant_word = pygame.image.load("assets/ant.png")
ant_logo = pygame.image.load("assets/ant_logo.png")
credits = pygame.transform.scale(pygame.image.load("assets/credits.png"), (500, 150))


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
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not play and play_button.get_rect(topleft=(450, 450)).collidepoint(event.pos):
                play = True
                snake1.reset(0, 0)
            elif play and back.get_rect(topleft=(10,10)).collidepoint(event.pos) or dead and back.get_rect(topleft=(10,10)).collidepoint(event.pos):
                play = False
                dead = False
                snake1.reset(0, 0)
                ant.col = 5
                ant.row = 5

    if not play and not dead:
        # Main Menu
        screen.fill((0, 0, 0))
        screen.blit(ant_logo, (550, 70))
        screen.blit(play_button, (450, 450))
        screen.blit(hack_club, (350, 190))
        screen.blit(credits, (450, 630))
    
    elif not dead: 
        # Game
        screen.fill((200, 200, 200))
        draw_grid(screen)
        ant.handle_held_movement()
        ant.update_animation()
        ant.draw(screen)
        snake1.chase(ant)
        screen.blit(ant_word, (300, 100))
        screen.blit(back, (10, 10))
        snake1.draw(screen)

    else:
        #Death screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        screen.blit(back, (10, 10))

    if ant.col == snake1.col and ant.row == snake1.row:
        play = False
        dead = True

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
