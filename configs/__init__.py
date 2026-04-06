# Configuration module
import yaml
import torch

# Load the config file
with open("simulation.yaml", "r") as f:
    config = yaml.safe_load(f)

# Logic for Option A: Explicit preference with fallback
preferred_device = config['training']['device']
if preferred_device == "cuda" and torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# Logic for Option B: Boolean flag
if config['hardware']['use_gpu'] and torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


