import argparse
import json
import matplotlib.pyplot as plt
import os

def plot_training_progress(jsonl_path, save_path, env_name):
    if not os.path.exists(jsonl_path):
        print(f"Error: Could not find '{jsonl_path}'")
        return

    timesteps = []
    returns = []

    # Read the JSON Lines file
    with open(jsonl_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                # Extract evaluation scores and timesteps
                if 'eval/returns' in data and 'eval/timesteps' in data:
                    timesteps.append(data['eval/timesteps'])
                    returns.append(data['eval/returns'])
            except json.JSONDecodeError:
                continue

    if not timesteps:
        print(f"No evaluation data found in '{jsonl_path}' yet!")
        return

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(timesteps, returns, marker='o', markersize=4, linestyle='-', color='blue')
    
    # Title formatted dynamically
    title = f"DreamerV3 Training Progress: {env_name.capitalize()}"
    plt.title(title, fontsize=14)
    
    plt.xlabel('Timesteps', fontsize=12)
    plt.ylabel('Evaluation Score', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Successfully generated graph: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot DreamerV3 Training Progress")
    parser.add_argument("--env", type=str, required=True, help="Game name (e.g., breakout, freeway, pong)")
    parser.add_argument("--log", type=str, default=None, help="Optional custom log path override")
    
    args = parser.parse_args()
    env_name = args.env.lower()
    
    # Determine the log path based on your folder structure
    if args.log:
        log_file = args.log
    else:
        # Automatically matches: rl_experiments/dreamerv3_<game>/results.jsonl
        log_file = f"rl_experiments/dreamerv3_{env_name}/results.jsonl"
        
        # Fallback to base dreamerv3 folder if game-specific folder isn't found
        if not os.path.exists(log_file) and os.path.exists("rl_experiments/dreamerv3/results.jsonl"):
            log_file = "rl_experiments/dreamerv3/results.jsonl"
    
    output_image = f"{env_name}_progress.png"
    plot_training_progress(log_file, output_image, args.env)