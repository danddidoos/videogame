import pygame
from constants import *

class Ant(pygame.sprite.Sprite):

    def __init__(self, col, row):
        self.col = col
        self.row = row
        x = self.col * TILE_SIZE + TILE_SIZE // 2
        y = self.row * TILE_SIZE + TILE_SIZE // 2

        self.direction = "RIGHT"

        self.frames = []
        for i in range(1,5):
            frame = pygame.image.load(f"assets/ant/ant_walk_{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))
            self.frames.append(frame)

        self.frame_index = 0.0
        self.animation_speed = 0.25
        self.is_moving = False

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.step_delay = 150
        self.last_step_time = 0

    def handle_held_movement(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        d_col, d_row = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = "LEFT"
            d_col = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = "RIGHT"
            d_col = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = "UP"
            d_row = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = "DOWN"
            d_row = 1

        if d_col != 0 or d_row != 0:
            self.is_moving = True
            if current_time - self.last_step_time >= self.step_delay:
                self.move(d_col, d_row)
                self.last_step_time = current_time
        else:
            self.is_moving = False

    def update_animation(self):
        if self.is_moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0.0
                self.is_moving = False
        else:
            self.frame_index = 0.0

    def move(self, d_col, d_row):
        new_col = self.col + d_col
        new_row = self.row + d_row

        if 0 <= new_col < GRID_COLS and 0 <= new_row < GRID_ROWS:
            self.col = new_col
            self.row = new_row
            self.is_moving = True

    def draw(self, surface):
        angles = {
            "RIGHT": -90,
            "DOWN": 180,
            "LEFT": 90,
            "UP": 0
        }

        current_frame = self.frames[int(self.frame_index)]

        rotated = pygame.transform.rotate(current_frame, angles.get(self.direction, 0))

        rect = rotated.get_rect(
            center=(
                self.col * TILE_SIZE + TILE_SIZE // 2,
                self.row * TILE_SIZE + TILE_SIZE // 2
            )
        )
        surface.blit(rotated, rect)
