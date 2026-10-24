import pygame
from constants import *

class Snake:
    def __init__(self, start_col=1, start_row=0, length=14, move_delay=300):
        self.length = length
        self.move_delay = move_delay
        self.last_move_time = 0

        self.body = [(start_col - i, start_row) for i in range(length)]

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

    def _get_exits(self, pos, obstacles):
        # Counts the number of neighbouring cells that are free from a position
        col, row = pos
        count = 0
        for d_col, d_row in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nc, nr = col + d_col, row + d_row
            if 0 <= nc < GRID_COLS and 0 <= nr < GRID_ROWS:
                if (nc, nr) not in obstacles:
                    count += 1
        return count
    
    def chase(self, target):
        current_time=pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_delay:
            return
        head_col, head_row = self.body[0]

        obstacles = set(self.body[:-1])

        all_neighbours = [
            (head_col + 1, head_row),
            (head_col - 1, head_row),
            (head_col, head_row + 1),
            (head_col, head_row - 1)
        ]

        valid_moves = []
        for col, row in all_neighbours:
            if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
                if (col, row) not in obstacles:
                    valid_moves.append((col, row))

        if not valid_moves:
            return

        # 2. Score each candidate by:
        #    a) exits: how many open tiles it will have after moving there
        #    b) dist: Manhattan distance to target
        scored_moves = []
        for move in valid_moves:
            # Simulate placing the head here; tail vacates body[-1]
            simulated_obstacles = (obstacles - {self.body[-1]}) | {move}
            exits = self._get_exits(move, simulated_obstacles)
            dist = abs(move[0] - target.col) + abs(move[1] - target.row)

            # Reaching target directly is an immediate win regardless of exits
            if move == (target.col, target.row):
                exits = 99

            scored_moves.append((move, exits, dist))

        # 3. Filter for safe moves (at least 2 escape exits to prevent dead ends)
        safe_moves = [m for m in scored_moves if m[1] >= 2]

        if safe_moves:
            # Pick the safe move that brings the snake closest to the ant
            safe_moves.sort(key=lambda item: item[2])
            chosen_move = safe_moves[0][0]
        else:
            # If all moves are tight/cornered, pick the move with the most exits
            scored_moves.sort(key=lambda item: (-item[1], item[2]))
            chosen_move = scored_moves[0][0]

        # 4. Apply movement
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
                else: 
                    angle = 0

                element = pygame.transform.rotate(self.head_image, angle)

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
                else: 
                    angle = 0

                element = pygame.transform.rotate(self.tail_image, angle)

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
                    element = pygame.transform.rotate(self.body_image, 90)

                # Case B: Vertical straight line (both neighbors share same column)
                elif p_dx == 0 and n_dx == 0:
                    element = self.body_image

                # Case C: Corner / Bend segment
                else:
                    neighbours = {(p_dx, p_dy), (n_dx, n_dy)}
                    if neighbours == {(0, 1), (1, 0)}:
                        element = pygame.transform.rotate(self.bend_image, -90)
                    elif neighbours == {(0, 1), (-1, 0)}:
                        element = pygame.transform.rotate(self.bend_image, 180)
                    elif neighbours == {(0, -1), (-1, 0)}:
                        element = pygame.transform.rotate(self.bend_image, 90)
                    elif neighbours == {(0, -1), (1, 0)}:
                        element = pygame.transform.rotate(self.bend_image, 0)
                    else:
                        element = self.body_image

            surface.blit(element, (pixel_x, pixel_y))

    def reset(self, start_col=0, start_row=0):
        if start_col == 0:
            start_col = -1

        self.body = [(start_col - i, start_row) for i in range(self.length)]
        self.last_move_time = 0