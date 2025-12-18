import random
import pygame

class Snake:
    def __init__(
        self,
        grid_left: int,
        grid_top: int,
        grid_width: int,
        grid_height: int,
        step: int = 50,
        initial_length: int = 5,
        segment_size: int | None = None,
    ) -> None:

        self.grid_left = grid_left
        self.grid_top = grid_top
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.step = step
        self.segment_size = step

        # Random starting cell inside the grid
        cols = grid_width // step
        rows = grid_height // step
        col_index = random.randint(0, cols - 1)
        row_index = random.randint(0, rows - 1)

        x = grid_left + col_index * step
        y = grid_top + row_index * step

        head = pygame.Rect(x, y, self.segment_size, self.segment_size)
        self.segments: list[pygame.Rect] = [head]

        # Start all stacked segments
        for _ in range(initial_length - 1):
            self.segments.append(pygame.Rect(x, y, self.segment_size, self.segment_size))

        self.direction: str | None = None
        self.alive = True

    # Update direction based on a key press
    def handle_key(self, key: int) -> None:
        if key == pygame.K_LEFT and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif key == pygame.K_RIGHT and self.direction != "LEFT":
            self.direction = "RIGHT"
        elif key == pygame.K_UP and self.direction != "DOWN":
            self.direction = "UP"
        elif key == pygame.K_DOWN and self.direction != "UP":
            self.direction = "DOWN"

    # Advance the snake one step
    def update(self) -> bool:
        if not self.alive:
            return False

        head = self.segments[0]
        new_x, new_y = head.x, head.y

        # Move one step in the current direction
        if self.direction == "LEFT":
            new_x = max(self.grid_left, head.x - self.step)
        elif self.direction == "RIGHT":
            new_x = min(self.grid_left + self.grid_width - head.width, head.x + self.step)
        elif self.direction == "UP":
            new_y = max(self.grid_top, head.y - self.step)
        elif self.direction == "DOWN":
            new_y = min(self.grid_top + self.grid_height - head.height, head.y + self.step)

        new_head = pygame.Rect(new_x, new_y, self.segment_size, self.segment_size)

        if self.direction is not None:
            # Wall collision
            if (
                new_head.x < self.grid_left
                or new_head.x > self.grid_left + self.grid_width - new_head.width
                or new_head.y < self.grid_top
                or new_head.y > self.grid_top + self.grid_height - new_head.height
            ):
                self.alive = False
                return False

            # Self collision
            if new_head in self.segments[1:]:
                self.alive = False
                return False

        # Update the snake's position
        self.segments = [new_head] + self.segments
        self.segments.pop()
        return True

    # Draw the snake
    def draw(self, surface: pygame.Surface, color: tuple[int, int, int]) -> None:
        for segment in self.segments:
            pygame.draw.rect(surface, color, segment)

