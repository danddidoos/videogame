import pygame
from constants import *

class Ant(pygame.sprite.Sprite):

    def __init__(self, col, row):
        self.col = col
        self.row = row
        x = self.col * TILE_SIZE + TILE_SIZE // 2
        y = self.row * TILE_SIZE + TILE_SIZE // 2

        self.direction = "RIGHT"
        # Temp code to be replaced when the actual ant image is made
        self.original_image = pygame.Surface((40,20), pygame.SRCALPHA)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))


    def move(self, d_col, d_row):
        new_col = self.col + d_col
        new_row = self.row + d_row

        if 0 <= new_col < GRID_COLS and 0 <= new_row < GRID_ROWS:
            self.col = new_col
            self.row = new_row

    def draw(self, surface):
        pixel_x = self.col * TILE_SIZE + 3
        pixel_y = self.row * TILE_SIZE + 3

        angles = {
            "RIGHT": 0,
            "DOWN": -90,
            "LEFT": 180,
            "UP": 90
        }

        rotated = pygame.transform.rotate(self.image, angles.get(self.direction, 0))

        rect = rotated.get_rect(
            center=(
                self.col * TILE_SIZE + TILE_SIZE // 2,
                self.row * TILE_SIZE + TILE_SIZE // 2
            )
        )
        surface.blit(rotated, rect)
