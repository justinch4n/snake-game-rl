# Snake Game Reinforced Learning
I made the classic snake game built with Pygame. You can control the snake with arrow keys to eat apples and grow longer while avoiding the barrier and self collision.

## Features

### Pygame Features

- Classic Snake gameplay
- Score tracking based on snake length
- Game over screen with play again option
- Grid based movement system
- Random apple spawning
- Collision detection of walls and self

### Reinforcement Learning Features

- Train an RL (DQN) agent to play Snake
- Deep Q Learning with model saving for replay and reward shaping
- Custom OpenAI Gym environment for Snake (`rl/snake_env.py`)
- Automatic saving of best and checkpoint models during training
- Log and visualize training progress with TensorBoard
- Play the game using a trained model or random agent with `rl/play_rl.py`


## Requirements

- Python 3.x
- pygame 2.6.1
- stable-baselines3
- gymnasium
- numpy
- torch
- tqdm


## Setup

### Virtual Environment

Create a virtual environment in the project root:

```bash
python3 -m venv .venv
```

Activate:

- **MacOS/Linux**: `source .venv/bin/activate`
- **Windows**: `.venv\Scripts\activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run Game for User

```bash
python main.py
```

### Controls

- **Arrow Keys**: Control the snake's direction
  - Up
  - Down
  - Left
  - Right

### Gameplay

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
├── entitySnake.py       # Snake class (movement, growth, collisions)
├── entityApple.py       # Apple class (spawning logic)
├── rl/                  # Reinforcement Learning module and code
│   ├── snake_env.py     # Gymnasium Snake RL environment
│   ├── train.py         # RL training script (contains DQN agent)
│   └── play_rl.py       # Script to play with RL agent or random actions
├── requirements.txt     # Python dependencies
└── README.md           # You are here
```

## Reinforcement Learning (RL)

This project includes a Gymnasium environment (`rl/snake_env.py`) for training RL agents to play Snake.

### Environment Details

- **Action Space**: `Discrete(4)` - Four discrete actions (UP, DOWN, LEFT, RIGHT)
- **Observation Space**: `Box(shape=(11,), low=-1.0, high=1.0)` meaning an 11-dimensional feature vector
  1-3 Apple position features (dx, dy, distance)
  4-6 Danger detection (straight, left, right)
  7-10 Current direction (one-hot encoding)
  11 Normalized snake length

### Training Components

#### DQN Agent (Deep Q-Network)

This project uses a DQN (Deep Q Network) agent. It's an RL algorithm that uses a neural network to learn which actions maximize long term rewards. It's also good with discrete action spaces such as this game.

**How it works:**

- **Q Function**: Learns to predict the expected future reward for each action in a given state
- **Experience Replay**: Stores past experiences (state, action, reward, next state) in a buffer and learns from random batches
- **Target Network**: Uses a separate network for stable learning
- **Exploration vs Exploitation**:
  - Starts with high exploration (ε=1.0, mostly random actions)
  - Gradually shifts to exploitation (ε=0.05, uses learned policy)

#### Monitor

The `Monitor` wrapper logs episode statistics to CSV files for analysis and visualization.

**What's tracked:**

- Episode rewards (total reward per episode)
- Episode lengths (number of steps per episode)
- Episode counts and timestamps

**Why it's useful:**

- Track training progress over time
- Compare different training runs
- Visualize learning curves
- Debug issues (e.g., rewards not improving)

**Output:** Saves data to `logs/monitor.csv` which can be plotted to see if the agent is improving.

#### Callbacks

Callbacks are functions that run during training to perform specific tasks at regular intervals.

**EvalCallback:**

- **Purpose**: Evaluates the agent's performance on a separate evaluation environment
- **When**: Runs every N steps (e.g., every 5,000 steps)
- **What it does**:
  - Tests the agent on a fresh environment (not used for training)
  - Saves the best performing model automatically
  - Logs evaluation metrics to `logs/eval/`
- **Why**: Prevents overfitting and tracks true performance (not just training performance)

**CheckpointCallback:**

- **Purpose**: Saves model checkpoints at regular intervals
- **When**: Saves every N steps (e.g., every 10,000 steps)
- **What it does**:
  - Saves model snapshots to `models/checkpoints/`
  - Allows resuming training if interrupted
  - Enables testing models at different training stages
- **Why**: Prevents losing progress if training crashes, and allows comparing models at different training stages

## Sources

For more information about:

- Gymnasium environments, see the [Gymnasium Env API documentation](https://gymnasium.farama.org/api/env/)
- Gymnasium spaces, see the [Gymnasium Spaces documentation](https://gymnasium.farama.org/api/spaces/)
