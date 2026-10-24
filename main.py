import pygame 

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
play = False
play_button = pygame.image.load("play.png")
hack_club = pygame.image.load("hack_club.png")
back = pygame.image.load("back.png")
ant_word = pygame.image.load("ant.png")
ant_logo = pygame.image.load("ant_logo.png")
credits = pygame.transform.scale(pygame.image.load("credits.png"), (500, 50))




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not play and play_button.get_rect(topleft=(200, 350)).collidepoint(event.pos):
                play = True
            elif play and back.get_rect(topleft=(10,10)).collidepoint(event.pos):
                play = False

    if not play:
        screen.fill((0, 0, 0))
        screen.blit(ant_logo, (300, 70))
        screen.blit(play_button, (200, 350))
        screen.blit(hack_club, (100, 190))
        screen.blit(credits, (200, 530))
    
    else:                
        screen.fill((200, 200, 200))
        screen.blit(ant_word, (300, 100))
        screen.blit(back, (10, 10))
        
    pygame.display.flip()
    clock.tick(60)


pygame.quit()