import sys
import pygame
from pygame.locals import *
from snake_entity import Snake
from apple_entity import Apple

# Init pygame
pygame.init() 

# Window size
W, H = 700, 700

# Colors
SNAKE_COLOR = (36, 140, 15)
APPLE_COLOR = (255, 0, 0)
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

# Snake configuration
STEP = 50
INITIAL_LENGTH = 5

snake = Snake(
    grid_left=GRID_LEFT,
    grid_top=GRID_TOP,
    grid_width=GRID_W,
    grid_height=GRID_H,
    step=STEP,
    initial_length=INITIAL_LENGTH,
)

apple = Apple(
    grid_left=GRID_LEFT,
    grid_top=GRID_TOP,
    grid_width=GRID_W,
    grid_height=GRID_H,
)

# Game loop
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            snake.handle_key(e.key)

    if not snake.update():
        pygame.quit()
        sys.exit()

    # Draw background and grid outline
    screen.fill(BG)
    pygame.draw.rect(screen, GRID_OUTLINE, (GRID_LEFT, GRID_TOP, GRID_W, GRID_H), width=2)

    # Draw the apple
    apple.draw(screen, APPLE_COLOR)

    # Draw the snake
    snake.draw(screen, SNAKE_COLOR)

    pygame.display.flip() # Update the display
    clock.tick(4) # 4 frames per second