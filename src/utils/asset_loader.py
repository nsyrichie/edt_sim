"""
Asset loading utilities.
"""

import torch
import numpy as np
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AssetManager:
    """Manages loading and caching of assets."""
    
    def __init__(self, asset_root: str = "assets"):
        """Initialize asset manager."""
        self.asset_root = Path(asset_root)
        self.cache = {}
        
        # Load asset configuration
        config_path = self.asset_root.parent / "configs" / "assets.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}
        
        logger.info(f"AssetManager initialized with root: {asset_root}")
    
    def load_mesh(self, mesh_name: str, device: str = "cpu") -> Optional[Dict[str, Any]]:
        """Load mesh from processed assets."""
        # Check cache first
        cache_key = f"{mesh_name}_{device}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Try different formats
        formats = ['.npz', '.glb', '.obj']
        mesh_data = None
        
        for fmt in formats:
            mesh_path = self.asset_root / "processed" / fmt[1:] / f"{mesh_name}{fmt}"
            if mesh_path.exists():
                if fmt == '.npz':
                    data = np.load(mesh_path, allow_pickle=True)
                    mesh_data = {
                        'vertices': torch.from_numpy(data['vertices']).to(device),
                        'faces': torch.from_numpy(data['faces']).to(device) if 'faces' in data else None,
                        'metadata': data.get('metadata', {}).item() if 'metadata' in data else {}
                    }
                elif fmt == '.glb':
                    # Placeholder for GLB loading
                    logger.info(f"GLB loading not fully implemented: {mesh_path}")
                    mesh_data = {'vertices': None, 'faces': None, 'metadata': {}}
                break
        
        if mesh_data:
            self.cache[cache_key] = mesh_data
            logger.info(f"Loaded mesh '{mesh_name}' from {fmt}")
        else:
            logger.warning(f"Mesh '{mesh_name}' not found")
        
        return mesh_data
    
    def load_agent(self, agent_type: str, device: str = "cpu") -> Optional[Dict[str, Any]]:
        """Load rigged agent with metadata."""
        mesh_data = self.load_mesh(agent_type, device)
        
        if not mesh_data:
            return None
        
        # Load rig data if available
        rig_path = self.asset_root / "processed" / "npz" / f"{agent_type}_rig.npz"
        if rig_path.exists():
            rig_data = np.load(rig_path, allow_pickle=True)
            mesh_data.update({
                'joints': torch.from_numpy(rig_data['joints']).to(device),
                'skin_weights': torch.from_numpy(rig_data['skin_weights']).to(device),
                'hierarchy': rig_data.get('hierarchy', {}).item()
            })
        
        return mesh_data
    
    def load_scene(self, scene_name: str, device: str = "cpu") -> Optional[Dict[str, Any]]:
        """Load environment scene."""
        return self.load_mesh(scene_name, device)