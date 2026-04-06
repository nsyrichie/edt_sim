"""
Agent controller for simulation.
"""

import torch
import torch.nn as nn
from typing import Dict, Any, Optional

class AgentController:
    """Agent controller for simulation."""
    
    def __init__(self, agent_id: str, config: Dict[str, Any], asset_manager, device: torch.device):
        """Initialize agent controller."""
        self.agent_id = agent_id
        self.config = config
        self.asset_manager = asset_manager
        self.device = device
        
        # Agent properties
        self.mass = config.get("mass", 1.0)
        self.action_dim = config.get("action_dim", 6)
        
        # State
        self.position = torch.zeros(3, device=device)
        self.velocity = torch.zeros(3, device=device)
        self.acceleration = torch.zeros(3, device=device)
        self.orientation = torch.eye(3, device=device)
        
        # Load mesh if specified
        self.mesh = None
        if "mesh_path" in config:
            self._load_mesh(config["mesh_path"])
        
        # Policy network
        self.policy = None
        
        print(f"AgentController '{agent_id}' initialized on {device}")
    
    def _load_mesh(self, mesh_path: str):
        """Load agent mesh."""
        self.mesh = self.asset_manager.load_mesh(mesh_path, self.device)
    
    def apply_action(self, action: torch.Tensor):
        """Apply action to agent."""
        if action.shape[0] >= 3:
            # Simple force-based control
            force = action[:3].to(self.device) * 10.0  # Scale force
            self.control_forces = force
    
    def get_state(self) -> Dict[str, torch.Tensor]:
        """Get current agent state."""
        return {
            "position": self.position,
            "velocity": self.velocity,
            "orientation": self.orientation
        }
    
    def get_joint_angles(self) -> torch.Tensor:
        """Get joint angles for rigged agent."""
        # Placeholder for joint angle extraction
        return torch.zeros(10, device=self.device)
    
    def get_sensor_readings(self, environment) -> Dict[str, torch.Tensor]:
        """Get sensor readings from environment."""
        return environment.get_sensor_readings(self.position)
    
    def get_observation(self) -> torch.Tensor:
        """Get observation for policy."""
        # Concatenate state information
        obs = torch.cat([
            self.position,
            self.velocity,
            self.orientation.flatten()
        ])
        return obs
    
    def reset(self):
        """Reset agent to initial state."""
        self.position = torch.zeros(3, device=self.device)
        self.velocity = torch.zeros(3, device=self.device)
        self.acceleration = torch.zeros(3, device=self.device)
        self.orientation = torch.eye(3, device=self.device)
        
        if hasattr(self, 'control_forces'):
            self.control_forces = torch.zeros(3, device=self.device)