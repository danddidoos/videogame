import pygame
import random
from constants import *

class Fruit:
    def __init__(self):
        self.col = 0
        self.row = 0

        self.image = pygame.transform.scale(pygame.image.load("assets/fruit.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self.respawn()

    def respawn(self, snake_body=None, ant_pos=None):
        if snake_body is None:
            snake_body = []
        while True:
            self.col = random.randint(0, GRID_COLS - 1)
            self.row = random.randint(0, GRID_ROWS - 1)
            if (self.col, self.row) not in snake_body and (ant_pos is None or (self.col, self.row) != ant_pos):
                break

    def draw(self, surface):
        pixel_x = self.col * TILE_SIZE
        pixel_y = self.row * TILE_SIZE
        surface.blit(self.image, (pixel_x, pixel_y))
        