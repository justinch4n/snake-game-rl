"""
Gymnasium environment for Snake game with feature-based state representation.
"""
import numpy as np  # for numerical operations
import gymnasium as gym  # for gymnasium environment
from gymnasium import spaces  # for action and observation spaces
from typing import Tuple, Dict, Any  # for type hints
import sys  # for system operations
import os  # for file operations
import math  # for mathematical operations

# Added parent directory to path to import game entities
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entitySnake import Snake
from entityApple import Apple


class SnakeEnv(gym.Env):
    """
    Gymnasium environment for Snake game with feature-based state representation.
    
    Observation space: 11-dimensional feature vector
    - [0-2]: Apple position features (dx, dy, distance)
    - [3-5]: Danger detection (straight, left, right)
    - [6-9]: Current direction (one-hot: up, down, left, right)
    - [10]: Normalized snake length
    
    Action space: Discrete(4)
    - 0: UP
    - 1: DOWN
    - 2: LEFT
    - 3: RIGHT
    """    
    # Initialize snake environment
    def __init__(
        self,
        grid_width: int = 600,
        grid_height: int = 600,
        step_size: int = 50,
        initial_length: int = 5,
        render_mode: str | None = None,
    ):
        # Initialize superclass gym
        super().__init__()

        # Initialize grid dimensions
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.step_size = step_size
        self.initial_length = initial_length
        
        # Grid dimensions (cols, rows, max_distance)
        self.grid_cols = grid_width / step_size
        self.grid_rows = grid_height / step_size

        # Max distance is the diagonal of the grid and used for normalization
        self.max_distance = math.sqrt(grid_width**2 + grid_height**2)
        
        # Grid boundaries (centered in 700x700 window, matching main.py)
        WINDOW_SIZE = 700
        self.grid_left = (WINDOW_SIZE - grid_width) // 2  # Centered horizontally
        self.grid_top = WINDOW_SIZE - grid_height - 50  # 50px from bottom
        self.grid_right = self.grid_left + grid_width
        self.grid_bottom = self.grid_top + grid_height
        
        # Define action space (4 possible moves aka the directions)
        self.action_space = spaces.Discrete(4)
        
        # Define observation space (11 features, range [-1, 1])
        self.observation_space = spaces.Box(-1, 1, shape=(11,))
        
        # Rendering
        self.render_mode = render_mode
        self.window = None
        self.clock = None
        self.screen = None
        
        # Initialize game state variables
        self.snake = None # Snake entity
        self.apple = None # Apple entity
        self.score = 0 # Score
        self.steps_without_food = 0 # Steps without food
        self.max_steps_without_food = 1000 # Prevent infinite games
    


    # Extract feature-based state representation
    def _get_obs(self) -> np.ndarray:
        """        
        Returns normalized feature vector:
            1. apple_dx: Normalized x distance to apple
            2. apple_dy: Normalized y distance to apple
            3. apple_distance: Normalized distance to apple
            4. danger_straight: 1 if danger ahead, 0 otherwise
            5. danger_left: 1 if danger to left, 0 otherwise
            6. danger_right: 1 if danger to right, 0 otherwise
            7. direction_up: 1 if moving up, 0 otherwise
            8. direction_down: 1 if moving down, 0 otherwise
            9. direction_left: 1 if moving left, 0 otherwise
            10. direction_right: 1 if moving right, 0 otherwise
            11. normalized_length: Snake length normalized by max possible length
        """
        # Case if snake or apple is not initialized
        if self.snake is None or self.apple is None:
            return np.zeros(11, dtype=np.float32)
        
        # Get snake head position
        head = self.snake.segments[0]
        
        # Convert pixel coordinates to grid coordinates
        head_col = head.x / self.step_size
        head_row = head.y / self.step_size
        apple_col = self.apple.x / self.step_size
        apple_row = self.apple.y / self.step_size
        
        # Calculate apple position features (dx, dy, distance)
        # Normalize by grid dimensions
        apple_dx = (apple_col - head_col) / self.grid_cols
        apple_dy = (apple_row - head_row) / self.grid_rows
        apple_dist = math.sqrt(apple_dx**2 + apple_dy**2) / self.max_distance

        # Calculate danger features (straight, left, right)
        danger_straight = self._check_danger((head_col, head_row), "UP")
        danger_left = self._check_danger((head_col, head_row), "LEFT")
        danger_right = self._check_danger((head_col, head_row), "RIGHT")
        
        # Calculate direction features (one-hot encoding)
        direction_up = 1 if self.snake.direction == "UP" else 0
        direction_down = 1 if self.snake.direction == "DOWN" else 0
        direction_left = 1 if self.snake.direction == "LEFT" else 0
        direction_right = 1 if self.snake.direction == "RIGHT" else 0
        
        # Calculate normalized snake length
        # Normalize by total cells on grid
        max_length = self.grid_cols * self.grid_rows  # Total cells on grid
        normalized_len = len(self.snake.segments) / max_length
        
        # Return numpy array with all 11 features
        return np.array([apple_dx, apple_dy, apple_dist, danger_straight, danger_left, danger_right, direction_up, direction_down, direction_left, direction_right, normalized_len], dtype=np.float32)
        


    # Check if moving in the given direction would result in collision
    def _check_danger(self, head_pos: Tuple[int, int], direction: str) -> bool:
        """        
        Returns True if danger of collision, False if safe
        """
        # Case if snake is not initialized or empty
        if self.snake is None or len(self.snake.segments) == 0:
            return False
        
        # Current head position in grid coordinates
        head_col, head_row = head_pos[0], head_pos[1]
        
        # Convert direction string to coordinate offsets
        direction_offsets = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }
        col_offset, row_offset = direction_offsets[direction]
        
        # Next position based on direction
        next_col = head_col + col_offset
        next_row = head_row + row_offset

        # Check wall collision (out of bounds)
        if next_col < 0 or next_col >= self.grid_cols or next_row < 0 or next_row >= self.grid_rows:
            return True
        
        # Check body collision (collision with snake segments)
        for segment in self.snake.segments[1:]:
            if segment.x / self.step_size == next_col and segment.y / self.step_size == next_row:
                return True
        
        # No collision
        return False
    

    
    # Get additional info
    def _get_info(self) -> Dict[str, Any]:
        """
        Returns dict with score, snake_length, steps_without_food
        """
        # Return info dictionary
        return {
             "score": self.score,
             "snake_length": len(self.snake.segments) if self.snake else 0,
             "steps_without_food": self.steps_without_food,
        }
        


    # Reset the environment to initial state
    def reset(self, seed: int | None = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Returns initial observation and info
        
        Args:
            seed: Random seed for reproducibility
        """
        super().reset(seed=seed)
        
        # Initialize Snake
        self.snake = Snake(
            grid_left=self.grid_left,
            grid_top=self.grid_top,
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            step=self.step_size,
            initial_length=self.initial_length,
        )
        
        # Initialize Apple
        self.apple = Apple(
            grid_left=self.grid_left,
            grid_top=self.grid_top,
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            cell_size=self.step_size,
            size=self.step_size,
        )
        
        # Spawn apple in valid position (not on snake)
        self.apple.spawn_random(self.snake.segments)
        
        # Set tracking variables
        self.score = 0
        self.steps_without_food = 0
        self.episode_steps = 0
        
        # Get initial observation and info
        observation = self._get_obs()
        info = self._get_info()
        
        # Render if needed
        if self.render_mode == "human":
            self._render_frame()
        
        # Return observation and info
        return observation, info
        

    
    # Execute one step in the environment
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Returns new observation, reward, terminated, truncated, info
        
        Args: action: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
        """
        # Convert action to int if it's a numpy array
        if isinstance(action, np.ndarray):
            action = int(action.item())
        else:
            action = int(action)
        
        # Convert action to direction string
        action_to_direction = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}
        direction = action_to_direction[action]
        
        # Set snake direction (prevent 180-degree turns)
        self.snake.direction_locked = False
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        
        if self.snake.direction is None:
            self.snake.direction = direction
        elif direction != opposites[self.snake.direction]:
            self.snake.next_direction = direction
            self.snake.direction_locked = True
        
        # Update snake and check if alive
        alive = self.snake.update()
        
        # Increment episode step counter
        self.episode_steps += 1
        
        # Initialize reward and termination flags
        reward = 0.0 # Reward for the action
        terminated = False # Episode ended (snake died or won)
        truncated = False # Episode ended to timeout
        
        # Calculate reward based on outcome
        if not alive:
            reward = -30.0 # Negative reward for dying
            terminated = True # Episode ended (snake died)

        elif self.apple.x == self.snake.segments[0].x and self.apple.y == self.snake.segments[0].y:
            reward = 5.0 # Positive reward for eating apple
            self.snake.grow() # Grow snake
            self.score += 100 # Increment score (100 points per apple)
            self.apple.spawn_random(self.snake.segments) # Spawn new apple
            self.steps_without_food = 0 # Reset counter

        elif len(self.snake.segments) == self.grid_cols * self.grid_rows:
            reward = 100.0 # Bonus reward for winning (filled grid)
            terminated = True # Episode ended (snake won)

        else:
            reward = -0.25 # Small negative reward per step
            self.steps_without_food += 1 # Increment steps without food
            
            # Truncate if too many steps without food
            if self.steps_without_food >= self.max_steps_without_food:
                reward = -10.0 # Penalty for inefficiency
                truncated = True
        
        # Get new observation and info
        observation = self._get_obs()
        info = self._get_info()
        
        # Render if needed
        if self.render_mode == "human":
            self._render_frame()
        
        # Return new observation, reward, terminated, truncated, info
        return observation, reward, terminated, truncated, info
    
    # Render the environment
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
    
    # Render a frame using pygame
    def _render_frame(self):
        if self.render_mode is None:
            return
        
        import pygame
        
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((700, 700))
            pygame.display.set_caption("Snake RL - Playing")
        
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        
        if self.screen is None:
            self.screen = pygame.Surface((700, 700))
        
        # Colors
        BG = (0, 0, 0)
        SNAKE_COLOR = (36, 140, 15)
        APPLE_COLOR = (255, 0, 0)
        GRID_OUTLINE = (60, 60, 60)
        
        # Draw background
        self.screen.fill(BG)
        pygame.draw.rect(
            self.screen,
            GRID_OUTLINE,
            (self.grid_left, self.grid_top, self.grid_width, self.grid_height),
            width=2,
        )
        
        # Draw apple
        if self.apple:
            self.apple.draw(self.screen, APPLE_COLOR)
        
        # Draw snake
        if self.snake:
            self.snake.draw(self.screen, SNAKE_COLOR)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        
        if self.render_mode == "human":
            self.window.blit(self.screen, self.window.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(10)  # 10 FPS for play (faster than training)
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )
    
    # Clean up resources
    def close(self):
        if self.window is not None:
            import pygame
            pygame.display.quit()
            pygame.quit()