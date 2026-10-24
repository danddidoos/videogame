import pygame
from constants import *

class Snake:
    def __init__(self):
        self.body = [(GRID_COLS // 2, GRID_ROWS // 2)]
        self.image = pygame.image.load("snake.png")
        self.position = (1, 0)
        self.row = 0
        self.col = 0

    def draw(self, screen):
        screen.blit(self.image, (self.position))

    def chase(self, target):
        if target.row < self.row:
            self.position[1] = -1
        elif target.row > self.row:
            self.position[1] = 1
        elif target.col < self.col:
            self.position[0] = -1
        elif target.col > self.col:
            self.position[0] = 1

