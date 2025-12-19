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

#Playfield (lower part of the screen)
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
    cell_size=STEP,
)

# Score tracking
score = 0
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

# Reset the game to initial state
def reset_game():
    global snake, apple
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
        cell_size=STEP,
    )

# Show play again dialog and return True if yes, False if no
def play_again_display(final_score):
    button_width = 150
    button_height = 50
    button_y = H // 2 + 80
    yes_x = W // 2 - button_width - 20
    no_x = W // 2 + 20
    
    yes_rect = pygame.Rect(yes_x, button_y, button_width, button_height)
    no_rect = pygame.Rect(no_x, button_y, button_width, button_height)
    
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_rect.collidepoint(mouse_pos):
                    return True
                elif no_rect.collidepoint(mouse_pos):
                    return False
        
        # Draw dialog
        screen.fill(BG)
        game_over_text = large_font.render("Game Over!", True, (255, 255, 255))
        score_text = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
        play_again_text = font.render("Play Again?", True, (255, 255, 255))
        
        text_rect1 = game_over_text.get_rect(center=(W // 2, H // 2 - 80))
        text_rect2 = score_text.get_rect(center=(W // 2, H // 2 - 30))
        text_rect3 = play_again_text.get_rect(center=(W // 2, H // 2 + 20))
        
        screen.blit(game_over_text, text_rect1)
        screen.blit(score_text, text_rect2)
        screen.blit(play_again_text, text_rect3)
        
        # Draw buttons
        pygame.draw.rect(screen, (0, 200, 0), yes_rect)
        pygame.draw.rect(screen, (200, 0, 0), no_rect)
        
        yes_text = font.render("Yes", True, (255, 255, 255))
        no_text = font.render("No", True, (255, 255, 255))
        
        yes_text_rect = yes_text.get_rect(center=yes_rect.center)
        no_text_rect = no_text.get_rect(center=no_rect.center)
        
        screen.blit(yes_text, yes_text_rect)
        screen.blit(no_text, no_text_rect)
        
        pygame.display.flip()
        clock.tick(60)

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
        # Calculate final score
        final_score = (len(snake.segments) - INITIAL_LENGTH) * 100
        
        # Show play again dialog
        if play_again_display(final_score):
            reset_game()
        else:
            pygame.quit()
            sys.exit()

    # Check if snake eats apple
    snake_head = snake.segments[0]
    apple_rect = pygame.Rect(apple.x, apple.y, apple.size, apple.size)
    if snake_head.colliderect(apple_rect):
        snake.grow()
        apple.spawn_random()
    
    # Calculate score based on snake length
    score = (len(snake.segments) - INITIAL_LENGTH) * 100

    # Draw background and grid outline
    screen.fill(BG)
    pygame.draw.rect(screen, GRID_OUTLINE, (GRID_LEFT, GRID_TOP, GRID_W, GRID_H), width=2)

    # Draw the apple
    apple.draw(screen, APPLE_COLOR)

    # Draw the snake
    snake.draw(screen, SNAKE_COLOR)
    
    # Draw the score at the top
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.flip() # Update the display
    clock.tick(4) # 4 frames per second