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

# snake is a list of rectangles
snake = [snake_head]

# Add 3 more rectangles to the snake
snake_length = 1
while snake_length < 5:
    snake_length += 1
    x = GRID_LEFT + col_index * STEP # Calculate the x position of the snake head
    y = GRID_TOP + row_index * STEP # Calculate the y position of the snake head
    snake.append(pygame.Rect(x, y, SNAKE_SIZE, SNAKE_SIZE))

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
                if direction != "RIGHT":
                    direction = "LEFT"
            elif e.key == pygame.K_RIGHT:
                if direction != "LEFT":
                    direction = "RIGHT"
            elif e.key == pygame.K_UP:
                if direction != "DOWN":
                    direction = "UP"
            elif e.key == pygame.K_DOWN:
                if direction != "UP":
                    direction = "DOWN"

    head = snake[0]
    newX = head.x
    newY = head.y

    # Update the head position based on the direction
    if direction == "LEFT":
        newX = max(GRID_LEFT, head.x - STEP)
    elif direction == "RIGHT":
        newX = min(GRID_LEFT + GRID_W - head.width, head.x + STEP)
    elif direction == "UP":
        newY = max(GRID_TOP, head.y - STEP)
    elif direction == "DOWN":
        newY = min(GRID_TOP + GRID_H - head.height, head.y + STEP)

    # Update the snake
    new_head = pygame.Rect(newX, newY, SNAKE_SIZE, SNAKE_SIZE)

    if direction is not None:
        # Check if the snake has hit the wall
        if new_head.x < GRID_LEFT or new_head.x > GRID_LEFT + GRID_W - new_head.width or new_head.y < GRID_TOP or new_head.y > GRID_TOP + GRID_H - new_head.height:
            pygame.quit()
            sys.exit()

        # Check if the snake has hit itself
        if new_head in snake[1:]:
            pygame.quit()
            sys.exit()
    
    snake = [new_head] + snake # Add the new head to the snake
    snake.pop() # Remove the last rectangle from the snake

    # Draw background and grid outline
    screen.fill(BG)
    pygame.draw.rect(screen, GRID_OUTLINE, (GRID_LEFT, GRID_TOP, GRID_W, GRID_H), width=2)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, segment) # Draw each segment of the snake

    pygame.display.flip() # Update the display
    clock.tick(4) # 4 frames per second