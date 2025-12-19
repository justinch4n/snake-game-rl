# Snake Game

The classic snake game built with Pygame. Control a snake with arrow keys to eat apples and grow longer while avoiding the barrier and self collision.

## Features

- Classic Snake gameplay
- Score tracking based on snake length
- Game over screen with play again option
- Grid based movement system
- Random apple spawning
- Collision detection of walls and self

## Requirements

- Python 3.x
- pygame 2.6.1

## Setup

### Virtual Environment

Create a virtual environment in the project root:

```bash
python3 -m venv .venv
```

Activate it:

- **MacOS/Linux**: `source .venv/bin/activate`
- **Windows**: `.venv\Scripts\activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

## Controls

- **Arrow Keys**: Control the snake's direction
  - Up
  - Down
  - Left
  - Right

## Gameplay

- The snake starts at a random position with an initial length of 5 segments (in same block)
- Use arrow keys to change direction (snake will continue in last pressed direction)
- Eat the red apples to grow longer and increase your score
- Avoid hitting the walls or your own tail
- Score increases by 100 points for each apple eaten
- When the game ends, you can choose to play again or exit

## Project Structure

```
snake-game-rl/
├── main.py              # Main game loop and pygame setup
├── snake_entity.py      # Snake class with movement and collision logic
├── apple_entity.py      # Apple class with random spawning
├── requirements.txt     # Python dependencies
└── README.md           # You are here
```

## Game Configuration

The game can be customized by modifying constants in `main.py`:

- `W, H`: Window size (default: 700x700)
- `GRID_W, GRID_H`: Playfield size (default: 600x600)
- `STEP`: Movement step size (default: 50)
- `INITIAL_LENGTH`: Starting snake length (default: 5)
- `clock.tick(4)`: Game speed (default: 4 FPS)
