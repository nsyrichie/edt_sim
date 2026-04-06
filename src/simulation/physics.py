"""
Physics engine for simulation.
"""

import torch
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class PhysicsEngine:
    """Physics simulation engine."""
    
    def __init__(self, config: Dict[str, Any], device: torch.device):
        """Initialize physics engine."""
        self.config = config
        self.device = device
        
        # Physics parameters
        self.gravity = torch.tensor(config.get("gravity", [0, -9.81, 0]), device=device)
        self.damping = config.get("damping", 0.99)
        
        # World state
        self.agents = {}
        self.static_bodies = []
        
        logger.info("Physics engine initialized")
    
    def add_agent(self, agent):
        """Add agent to physics world."""
        self.agents[agent.agent_id] = agent
        logger.info(f"Added agent '{agent.agent_id}' to physics world")
    
    def step(self, dt: float):
        """Step physics simulation."""
        # Apply forces
        self._apply_forces(dt)
        
        # Update velocities
        self._update_velocities(dt)
        
        # Update positions
        self._update_positions(dt)
        
        # Apply damping
        self._apply_damping(dt)
    
    def _apply_forces(self, dt: float):
        """Apply forces to all bodies."""
        for agent in self.agents.values():
            # Gravity
            force = agent.mass * self.gravity
            
            # Control forces
            if hasattr(agent, 'control_forces'):
                force += agent.control_forces
            
            # Update acceleration
            agent.acceleration = force / agent.mass
    
    def _update_velocities(self, dt: float):
        """Update velocities based on acceleration."""
        for agent in self.agents.values():
            agent.velocity += agent.acceleration * dt
    
    def _update_positions(self, dt: float):
        """Update positions based on velocities."""
        for agent in self.agents.values():
            agent.position += agent.velocity * dt
    
    def _apply_damping(self, dt: float):
        """Apply velocity damping."""
        for agent in self.agents.values():
            agent.velocity *= self.damping
    
    def reset(self):
        """Reset physics state."""
        for agent in self.agents.values():
            agent.velocity = torch.zeros(3, device=self.device)
            agent.acceleration = torch.zeros(3, device=self.device)