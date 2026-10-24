import pygame
from constants import *

class Snake:
    def __init__(self, start_col=0, start_row=0, length=14, move_delay=300):
        self.length = length
        self.move_delay = move_delay
        self.last_move_time = 0

        self.body = []
        for i in range(length):
            c = max(0, start_col - i)
            self.body.append((c, start_row))

        self.head_image = pygame.transform.scale(pygame.image.load("assets/snake/snake_head.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self.body_image = pygame.transform.scale(pygame.image.load("assets/snake/snake_body_line.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self.bend_image = pygame.transform.scale(pygame.image.load("assets/snake/snake_body_bend.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self.tail_image = pygame.transform.scale(pygame.image.load("assets/snake/snake_tail.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))

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
            # 1. Skip drawing if off-screen
            if col < 0 or col >= GRID_COLS or row < 0 or row >= GRID_ROWS:
                continue

            pixel_x = col * TILE_SIZE
            pixel_y = row * TILE_SIZE

            if i == 0:
                # Head
                next_seg = self.body[1]
                dx = col - next_seg[0]
                dy = row - next_seg[1]

                if dx == 1: 
                    angle = -90
                elif dx == -1: 
                    angle = 90
                elif dy == 1: 
                    angle = 180
                else: angle = 0

                rotated = pygame.transform.rotate(self.head_image, angle)
                surface.blit(rotated, (pixel_x, pixel_y))

            elif i == len(self.body) - 1:
                # Tail
                prev_seg = self.body[i - 1]
                dx = prev_seg[0] - col
                dy = prev_seg[1] - row

                if dx == 1: 
                    angle = -90
                elif dx == -1: 
                    angle = 90 
                elif dy == 1: 
                    angle = 180
                elif dy == -1: 
                    angle = 0

                rotated = pygame.transform.rotate(self.tail_image, angle)
                surface.blit(rotated, (pixel_x, pixel_y))

            else:
                # Body
                prev_seg = self.body[i - 1]
                next_seg = self.body[i + 1]

                p_dx = prev_seg[0] - col
                p_dy = prev_seg[1] - row
                n_dx = next_seg[0] - col
                n_dy = next_seg[1] - row

                # Skip/ignore overlapping segments (e.g. at spawn)
                if (p_dx == 0 and p_dy == 0) or (n_dx == 0 and n_dy == 0):
                    continue

                # Case A: Horizontal straight line (both neighbors share same row)
                if p_dy == 0 and n_dy == 0:
                    rotated = pygame.transform.rotate(self.body_image, 90)

                # Case B: Vertical straight line (both neighbors share same column)
                elif p_dx == 0 and n_dx == 0:
                    rotated = pygame.transform.rotate(self.body_image, 0)

                # Case C: Corner / Bend segment
                else:
                    neighbours = {(p_dx, p_dy), (n_dx, n_dy)}
                    if neighbours == {(0, 1), (1, 0)}:
                        rotated = pygame.transform.rotate(self.bend_image, -90)
                    elif neighbours == {(0, 1), (-1, 0)}:
                        rotated = pygame.transform.rotate(self.bend_image, 180)
                    elif neighbours == {(0, -1), (-1, 0)}:
                        rotated = pygame.transform.rotate(self.bend_image, 90)
                    elif neighbours == {(0, -1), (1, 0)}:
                        rotated = pygame.transform.rotate(self.bend_image, 0)
                    else:
                        rotated = self.body_image

                surface.blit(rotated, (pixel_x, pixel_y))

    def reset(self, start_col=0, start_row=0):
        self.body = []
        for i in range(self.length):
            c = max(0, start_col - i)
            self.body.append((c, start_row))
        self.last_move_time = 0
