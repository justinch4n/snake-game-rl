import pygame
from pygame.locals import *
import random
import sys


# Init pygame
pygame.init() 

# Window size
W, H = 700, 700

# Colors
SNAKE_COLOR = (36, 140, 15)
BG = (0, 0, 0)
GRID_OUTLINE = (60, 60, 60)

# Screen setup
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Classic Snake Game")

# Clock
clock = pygame.time.Clock()

# Bottom playfield: 600x600 grid constrained area
GRID_W, GRID_H = 600, 600
GRID_LEFT = (W - GRID_W) // 2
GRID_TOP = H - GRID_H - 50

# Snake head
SNAKE_SIZE = 50
STEP = 50 # Step is one cell size
COLS = GRID_W // STEP # Number of columns in the grid
ROWS = GRID_H // STEP # Number of rows in the grid

# Randomly select a cell in the grid
col_index  = random.randint(0, COLS - 1) # Randomly select a column in the grid
row_index = random.randint(0, ROWS - 1) # Randomly select a row in the grid

x = GRID_LEFT + col_index * STEP # Calculate the x position of the snake head
y = GRID_TOP + row_index * STEP # Calculate the y position of the snake head

snake_head = pygame.Rect(x, y, SNAKE_SIZE, SNAKE_SIZE)
direction = None

# Game loop
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Update direction
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                direction = "LEFT"
            elif e.key == pygame.K_RIGHT:
                direction = "RIGHT"
            elif e.key == pygame.K_UP:
                direction = "UP"
            elif e.key == pygame.K_DOWN:
                direction = "DOWN"
    
    if direction == "LEFT":
        snake_head.x = max(GRID_LEFT, snake_head.x - STEP)
    elif direction == "RIGHT":
        snake_head.x = min(GRID_LEFT + GRID_W - snake_head.width, snake_head.x + STEP)
    elif direction == "UP":
        snake_head.y = max(GRID_TOP, snake_head.y - STEP)
    elif direction == "DOWN":
        snake_head.y = min(GRID_TOP + GRID_H - snake_head.height, snake_head.y + STEP)

    # Draw background and grid outline
    screen.fill(BG)
    pygame.draw.rect(screen, GRID_OUTLINE, (GRID_LEFT, GRID_TOP, GRID_W, GRID_H), width=2)

    # Draw snake head
    pygame.draw.rect(screen, SNAKE_COLOR, snake_head)

    pygame.display.flip() # Update the display
    clock.tick(2) # 2 frames per second