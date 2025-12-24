"""
Training script for Snake RL agent using DQN.
"""
from typing import Any


import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stable_baselines3 import DQN # for DQN agent
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback # for callbacks
from stable_baselines3.common.monitor import Monitor # for monitoring environment
from rl import SnakeEnv # for SnakeEnv environment

# Main training function
def main():    
    # Create training environment
    env = SnakeEnv(
        grid_width=600,
        grid_height=600,
        step_size=50,
        initial_length=5,
    )
    
    # Wrap with Monitor for logging
    log_dir = "logs/"
    os.makedirs(log_dir, exist_ok=True)
    env = Monitor(env, log_dir)
    
    # Create evaluation environment
    eval_env = SnakeEnv(
        grid_width=600,
        grid_height=600,
        step_size=50,
        initial_length=5,
        render_mode=None,
    )
    # Wrap with Monitor for logging
    eval_env = Monitor[Any, Any](eval_env, log_dir + "eval/")
    
    # Create DQN agent
    model = DQN(
        "MlpPolicy",  # Multi-layer perceptron policy
        env,
        learning_rate=1e-4,
        learning_starts=1000, # Steps before learning starts
        batch_size=32, # Batch size for training
        tensorboard_log="tensorboard_logs/", # for logging rewards and losses
        gamma=0.99, # Discount factor for future rewards
        buffer_size=100_000, # Replay buffer size
        exploration_fraction=0.2,   # Exploration phase fraction
        exploration_initial_eps=1.0, # Initial exploration rate
        exploration_final_eps=0.05, # Final exploration rate

    )
    
    # Set up callbacks
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path="models/best/",
        log_path=log_dir + "eval/",
        eval_freq=5000,  # Evaluate every N steps
        deterministic=True,
        render=False,
    )
    
    checkpoint_callback = CheckpointCallback(
        save_freq=10000,  # Save checkpoint every N steps
        save_path="models/checkpoints/",
        name_prefix="snake_dqn",
    )
    
    # Train the agent
    print("Starting training...")
    model.learn(
        total_timesteps=5000000,  # Total training steps
        callback=[eval_callback, checkpoint_callback],
        progress_bar=True,
    )
    
    # Save final model
    model.save("models/snake_dqn_final")
    print("Training complete! Model saved to models/snake_dqn_final")

if __name__ == "__main__":
    main()