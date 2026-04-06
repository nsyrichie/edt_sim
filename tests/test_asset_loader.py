"""
Unit tests for asset loader.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from utils.asset_loader import AssetManager

class TestAssetLoader(unittest.TestCase):
    """Test cases for AssetManager."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.asset_manager = AssetManager("assets")
    
    def test_initialization(self):
        """Test asset manager initialization."""
        self.assertIsNotNone(self.asset_manager)
        self.assertEqual(self.asset_manager.asset_root, Path("assets"))
    
    def test_load_mesh_not_found(self):
        """Test loading non-existent mesh."""
        mesh = self.asset_manager.load_mesh("non_existent_mesh")
        self.assertIsNone(mesh)
    
    def test_cache_functionality(self):
        """Test caching works."""
        # Load mesh (will be None but should be cached)
        self.asset_manager.load_mesh("test_mesh")
        self.assertIn("test_mesh_cpu", self.asset_manager.cache)

if __name__ == "__main__":
    unittest.main()