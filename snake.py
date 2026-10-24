import pygame
from constants import *

class Snake:
    def __init__(self):
        self.body = [(GRID_COLS // 2, GRID_ROWS // 2)]
        self.image = pygame.image.load("snake.png")
        self.direction = (1, 0)

    def draw(self, screen):
        for segment in self.body:
            screen.blit(self.image, (segment[0] * TILE_SIZE, segment[1] * TILE_SIZE))
            