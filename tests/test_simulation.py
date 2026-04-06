"""
Unit tests for simulation core.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from simulation.core import Simulation

class TestSimulation(unittest.TestCase):
    """Test cases for Simulation class."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.config_path = "configs/simulation.yaml"
    
    def test_initialization(self):
        """Test simulation initialization."""
        sim = Simulation(self.config_path, device="cpu")
        self.assertIsNotNone(sim)
        self.assertEqual(sim.current_step, 0)
    
    def test_add_agent(self):
        """Test adding agents to simulation."""
        sim = Simulation(self.config_path, device="cpu")
        sim.add_agent("test_agent", {"action_dim": 6})
        self.assertIn("test_agent", sim.agents)
    
    def test_reset_functionality(self):
        """Test simulation reset."""
        sim = Simulation(self.config_path, device="cpu")
        sim.add_agent("test_agent", {"action_dim": 6})
        sim.step()
        sim.reset()
        self.assertEqual(sim.current_step, 0)

if __name__ == "__main__":
    unittest.main()