"""
Learning components for agents.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class PolicyNetwork(nn.Module):
    """Policy network for agent control."""
    
    def __init__(self, state_dim: int = 24, action_dim: int = 6, hidden_dim: int = 128):
        """Initialize policy network."""
        super().__init__()
        
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # Output in [-1, 1]
        )
        
        # Learnable log standard deviation
        self.log_std = nn.Parameter(torch.zeros(action_dim))
    
    def forward(self, state: torch.Tensor, deterministic: bool = False):
        """Forward pass."""
        mean = self.network(state)
        
        if deterministic:
            return mean
        
        std = torch.exp(self.log_std)
        normal = torch.distributions.Normal(mean, std)
        action = normal.rsample()
        
        return action, normal.log_prob(action).sum(-1)
    
    def get_action(self, state: torch.Tensor, deterministic: bool = False) -> torch.Tensor:
        """Get action from policy."""
        with torch.no_grad():
            if deterministic:
                return self.forward(state, deterministic=True)
            else:
                action, _ = self.forward(state, deterministic=False)
                return action


class ValueNetwork(nn.Module):
    """Value network for critic."""
    
    def __init__(self, state_dim: int = 24, hidden_dim: int = 128):
        """Initialize value network."""
        super().__init__()
        
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        return self.network(state)