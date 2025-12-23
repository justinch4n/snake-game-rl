import random
import pygame

class Apple:
    def __init__(
        self,
        grid_left: int,
        grid_top: int,
        grid_width: int,
        grid_height: int,
        cell_size: int = 50,
        size: int = 30,
    ) -> None:

        self.grid_left = grid_left
        self.grid_top = grid_top
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.size = size

        # Spawn the apple at a random position (without snake segments initially)
        self.spawn_random([])

    def spawn_random(self, snake_segments: list = None) -> None:
        if snake_segments is None:
            snake_segments = []
        cols = self.grid_width // self.cell_size
        rows = self.grid_height // self.cell_size

        # Try to find a valid position (not occupied by snake)
        max_attempts = cols * rows * 2  # Prevent infinite loop
        attempts = 0
        
        while attempts < max_attempts:
            col = random.randint(0, cols - 1)
            row = random.randint(0, rows - 1)

            # top left of the chosen cell
            cell_left = self.grid_left + col * self.cell_size
            cell_top = self.grid_top + row * self.cell_size

            # Create a rect for this cell to check collision
            cell_rect = pygame.Rect(cell_left, cell_top, self.cell_size, self.cell_size)
            
            # Check if this cell collides with any snake segment
            collision = False
            for segment in snake_segments:
                if cell_rect.colliderect(segment):
                    collision = True
                    break
            
            # If no collision, use this position
            if not collision:
                # center the apple (size) inside the cell (cell_size)
                offset = (self.cell_size - self.size) // 2
                self.x = cell_left + offset
                self.y = cell_top + offset
                return
            
            attempts += 1
        
        raise ValueError("No valid position found for apple")

    # Draw the apple
    def draw(self, surface: pygame.Surface, color: tuple[int, int, int]) -> None:
        pygame.draw.rect(surface, color, pygame.Rect(self.x, self.y, self.size, self.size))



