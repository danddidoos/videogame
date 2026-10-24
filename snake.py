import pygame
from constants import *

class Snake:
    def __init__(self, move_delay = 300):
        self.body = [(GRID_COLS // 2, GRID_ROWS // 2)]
        self.image = pygame.transform.scale(pygame.image.load("assets/snake.png"), (900, TILE_SIZE * 3))
        self.position = [1, 0]
        self.row = 0
        self.col = 0
        self.move_delay = move_delay
        self.last_move_time = 0

    def draw(self, screen):
        screen.blit(self.image, (self.col * TILE_SIZE, self.row * TILE_SIZE))

    def chase(self, target):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            if target.row < self.row:
                self.row -= 1
            elif target.row > self.row:
                self.row += 1
            elif target.col < self.col:
                self.col -= 1
            elif target.col > self.col:
                self.col += 1

            self.last_move_time = current_time

