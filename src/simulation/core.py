"""
Core simulation manager.
"""

import torch
import yaml
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from .physics import PhysicsEngine
from .renderer import Renderer
from ..agents.controller import AgentController
from ..utils.asset_loader import AssetManager

logger = logging.getLogger(__name__)

class Simulation:
    """Main simulation manager."""
    
    def __init__(self, config_path: str, device: str = "cuda"):
        """Initialize simulation."""
        self.config = self._load_config(config_path)
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        
        # Initialize components
        self.asset_manager = AssetManager(self.config.get("assets_root", "assets"))
        self.physics = None
        self.renderer = None
        self.agents = {}
        
        # Simulation state
        self.current_step = 0
        self.max_steps = self.config.get("max_steps", 10000)
        self.dt = self.config.get("dt", 0.01)
        
        self._setup()
        logger.info(f"Simulation initialized on {self.device}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _setup(self):
        """Setup simulation components."""
        # Setup physics
        self.physics = PhysicsEngine(
            self.config.get("physics", {}),
            self.device
        )
        
        # Setup renderer if enabled
        if self.config.get("enable_rendering", False):
            self.renderer = Renderer(
                self.config.get("renderer", {}),
                self.device
            )
    
    def add_agent(self, agent_id: str, config: Dict[str, Any]):
        """Add an agent to simulation."""
        agent = AgentController(
            agent_id=agent_id,
            config=config,
            asset_manager=self.asset_manager,
            device=self.device
        )
        
        self.physics.add_agent(agent)
        self.agents[agent_id] = agent
        logger.info(f"Added agent '{agent_id}' to simulation")
    
    def step(self, actions: Optional[Dict[str, torch.Tensor]] = None) -> Dict[str, Any]:
        """Execute one simulation step."""
        self.current_step += 1
        
        # Apply actions
        if actions:
            for agent_id, action in actions.items():
                if agent_id in self.agents:
                    self.agents[agent_id].apply_action(action)
        
        # Update physics
        self.physics.step(self.dt)
        
        # Get observations
        observations = self._get_observations()
        
        # Render if enabled
        if self.renderer and self.current_step % self.config.get("render_interval", 1) == 0:
            frames = self.renderer.render(self.agents)
        
        return observations
    
    def _get_observations(self) -> Dict[str, torch.Tensor]:
        """Get current observations for all agents."""
        observations = {}
        for agent_id, agent in self.agents.items():
            observations[agent_id] = {
                "position": agent.position.clone(),
                "velocity": agent.velocity.clone(),
                "orientation": agent.orientation.clone()
            }
        return observations
    
    def run(self, steps: Optional[int] = None) -> List[Dict[str, Any]]:
        """Run simulation for specified number of steps."""
        steps = steps or self.max_steps
        history = []
        
        logger.info(f"Running simulation for {steps} steps")
        
        for step in range(steps):
            # Generate random actions for demo
            actions = {
                agent_id: torch.randn(agent.action_dim, device=self.device)
                for agent_id, agent in self.agents.items()
            }
            
            # Step simulation
            observations = self.step(actions)
            history.append(observations)
            
            # Log progress
            if (step + 1) % 100 == 0:
                logger.info(f"Step {step + 1}/{steps}")
        
        logger.info(f"Simulation completed: {len(history)} steps")
        return history
    
    def reset(self):
        """Reset simulation to initial state."""
        logger.info("Resetting simulation")
        self.current_step = 0
        
        for agent in self.agents.values():
            agent.reset()
        
        self.physics.reset()