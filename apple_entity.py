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

        # Spawn the apple at a random position
        self.spawn_random()

    def spawn_random(self) -> None:
        cols = self.grid_width // self.cell_size
        rows = self.grid_height // self.cell_size

        col = random.randint(0, cols - 1)
        row = random.randint(0, rows - 1)

        # top left of the chosen cell
        cell_left = self.grid_left + col * self.cell_size
        cell_top = self.grid_top + row * self.cell_size

        # center the apple (size) inside the cell (cell_size)
        offset = (self.cell_size - self.size) // 2
        self.x = cell_left + offset
        self.y = cell_top + offset

    # Draw the apple
    def draw(self, surface: pygame.Surface, color: tuple[int, int, int]) -> None:
        pygame.draw.rect(surface, color, pygame.Rect(self.x, self.y, self.size, self.size))



