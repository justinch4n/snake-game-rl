"""
Play the game using a trained RL model or random actions.
"""
import sys # for system operations
import os # for file operations

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse # for command line arguments
from rl import SnakeEnv # for SnakeEnv environment
from stable_baselines3 import DQN # for DQN agent

# Play using random actions
def play_random(env, num_episodes=1):
    # Print message about random play
    print(f"Playing with random actions for {num_episodes} episodes...")
    
    # Loop for num_episodes
    for episode in range(num_episodes):
        obs, info = env.reset()
        # Initialize tracking variables
        total_reward = 0
        steps = 0
        terminated = False
        truncated = False

        # Run episode loop
        while not terminated and not truncated:
            # Sample random action from action_space
            action = env.action_space.sample()
            # Take step
            obs, reward, terminated, truncated, info = env.step(action)
            # Accumulate reward
            total_reward += reward
            steps += 1
        # Print episode results
        print(f"Episode {episode+1}: Total Reward = {total_reward}, Steps = {steps}")


# Play using a trained model
def play_with_model(env, model_path, num_episodes=1):
    # Try to load model from stable_baselines3
    try:
        model = DQN.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Falling back to random actions...")
        play_random(env, num_episodes)
        return
    
    # Print message about playing with model
    print(f"Playing with model from {model_path} for {num_episodes} episodes...")
    
    # Loop for num_episodes
    for episode in range(num_episodes):
        obs, info = env.reset()
        # Initialize tracking variables
        total_reward = 0
        steps = 0
        terminated = False
        truncated = False

        # Run episode loop
        while not terminated and not truncated:
            # Get action from model (predict returns tuple: action, state)
            action, _ = model.predict(obs, deterministic=True)
            action = int(action)  # Convert to int
            # Take step
            obs, reward, terminated, truncated, info = env.step(action)
            # Accumulate reward
            total_reward += reward
            steps += 1
        # Print episode results
        print(f"Episode {episode+1}: Score={info['score']}, Steps={steps}, Reward={total_reward:.2f}")

# Main function to parse arguments and run play
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="nake with RL agent")
    parser.add_argument("--model", type=str, default=None, help="Path to trained model")
    parser.add_argument("--episodes", type=int, default=1, help="Number of episodes")
    args = parser.parse_args()

    # Initialize environment
    env = SnakeEnv(
        grid_width=600,
        grid_height=600,
        step_size=50,
        initial_length=5,
    )
    
    # Play with model or random
    try:
        if args.model:
            play_with_model(env, args.model, args.episodes)
        else:
            play_random(env, args.episodes)
    finally:
        env.close()
    

if __name__ == "__main__":
    main()
