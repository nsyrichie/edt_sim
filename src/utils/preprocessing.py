"""
Asset preprocessing utilities.
"""

import numpy as np
from pathlib import Path
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class AssetPreprocessor:
    """Preprocess assets for simulation."""
    
    def __init__(self, input_dir: str = "assets/blender", output_dir: str = "assets/processed"):
        """Initialize preprocessor."""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "glb").mkdir(exist_ok=True)
        (self.output_dir / "npz").mkdir(exist_ok=True)
        
        logger.info(f"AssetPreprocessor initialized")
    
    def process_mesh(self, input_path: Path, output_name: str, 
                    scale: float = 1.0, center: bool = True) -> bool:
        """Process mesh file."""
        try:
            # Create dummy mesh for demo
            vertices = np.array([
                [-0.5, -0.5, 0],
                [0.5, -0.5, 0],
                [0, 0.5, 0]
            ], dtype=np.float32) * scale
            
            faces = np.array([[0, 1, 2]], dtype=np.int32)
            
            if center:
                vertices = vertices - vertices.mean(axis=0)
            
            # Save as npz
            output_path = self.output_dir / "npz" / f"{output_name}.npz"
            np.savez(output_path, 
                    vertices=vertices, 
                    faces=faces,
                    metadata={"source": str(input_path), "scale": scale})
            
            logger.info(f"Processed {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process {input_path}: {e}")
            return False
    
    def batch_process(self, file_pattern: str = "**/*.blend") -> List[str]:
        """Process all matching files."""
        processed = []
        
        for blend_file in self.input_dir.glob(file_pattern):
            if blend_file.is_file():
                output_name = blend_file.stem
                success = self.process_mesh(blend_file, output_name)
                if success:
                    processed.append(str(blend_file))
        
        logger.info(f"Processed {len(processed)} files")
        return processed
    
    def create_example_assets(self):
        """Create example assets for testing."""
        # Create example agent
        agent_dir = self.output_dir / "npz"
        
        # Simple cube mesh
        vertices = np.array([
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5]
        ], dtype=np.float32)
        
        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # Front
            [4, 6, 5], [4, 7, 6],  # Back
            [0, 4, 1], [1, 4, 5],  # Bottom
            [2, 6, 3], [3, 6, 7],  # Top
            [0, 3, 4], [3, 7, 4],  # Left
            [1, 5, 2], [2, 5, 6]   # Right
        ], dtype=np.int32)
        
        np.savez(agent_dir / "example_agent.npz",
                vertices=vertices,
                faces=faces,
                metadata={"type": "example", "vertices": 8, "faces": 12})
        
        logger.info(f"Created example asset at {agent_dir / 'example_agent.npz'}")