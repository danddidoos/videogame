import pygame 

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
play = False
play_button = pygame.image.load("play.png")
title = pygame.image.load("wordle.png")
begin_guessing = pygame.image.load("begin_guessing.png")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.get_rect(topleft=(300, 400)).collidepoint(event.pos):
                play = True

    screen.fill((0, 0, 0))
    screen.blit(title, (300, 100))
    screen.blit(play_button, (300, 400))
    pygame.display.flip()
    clock.tick(60)
    while play == True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        screen.fill((200, 200, 200))
        screen.blit(begin_guessing, (300, 100))
        pygame.display.flip()

pygame.quit()