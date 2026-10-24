import pygame
from constants import *

class Snake:
    def __init__(self, start_col=0, start_row=0, length=20, move_delay=200):
        self.length = length
        self.move_delay = move_delay
        self.last_move_time = 0

        self.body = []
        for i in range(length):
            c = max(0, start_col - i)
            self.body.append((c, start_row))

        self.head_image = pygame.transform.scale(pygame.image.load("assets/snake/snake_head.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self.body_image = pygame.transform.scale(pygame.image.load("assets/snake/snake_body_line.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))

    @property
    def col(self):
        return self.body[0][0]
    @property
    def row(self):
        return self.body[0][1]

    def set_pos(self, col, row):
        self.body[0] = (col, row)

    def chase(self, target):
        current_time=pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_delay:
            return
        head_col, head_row = self.body[0]
        target_moves = []
        if target.col < head_col:
            target_moves.append((head_col -1, head_row))
        elif target.col > head_col:
            target_moves.append((head_col + 1, head_row))
        if target.row < head_row:
            target_moves.append((head_col, head_row - 1))
        elif target.row > head_row:
            target_moves.append((head_col, head_row + 1))

        all_neighbours = [
            (head_col + 1, head_row),
            (head_col - 1, head_row),
            (head_col, head_row + 1),
            (head_col, head_row - 1)
        ]

        move_candidates = target_moves + [m for m in all_neighbours if m not in target_moves]

        chosen_move = None
        for move in move_candidates:
            col, row = move
            if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
                if (col, row) not in self.body[:-1]:
                    chosen_move = move
                    break
        if chosen_move:
            self.last_move_time = current_time
            self.body.insert(0, chosen_move)
            if len(self.body) > self.length:
                self.body.pop()


    def draw(self, surface):
        for i, (col, row) in enumerate(self.body):
            pixel_x = col * TILE_SIZE
            pixel_y = row * TILE_SIZE
            if i == 0:
                surface.blit(self.head_image, (pixel_x, pixel_y))
            else:
                surface.blit(self.body_image, (pixel_x, pixel_y))

    def reset(self, start_col=0, start_row=0):
        self.body = []
        for i in range(self.length):
            c = max(0, start_col - i)
            self.body.append((c, start_row))
        self.last_move_time = 0
