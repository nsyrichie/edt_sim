#!/usr/bin/env python3
"""
Blender export script for asset conversion.
"""

import sys
import json
import argparse
from pathlib import Path

def export_blender_assets(blend_path: str, output_path: str, export_format: str = "glb"):
    """
    Export Blender assets to simulation format.
    
    This script is meant to be run from within Blender:
    blender --background --python export_blender.py -- --input scene.blend --output exported.glb
    """
    
    try:
        import bpy
    except ImportError:
        print("This script must be run from within Blender")
        print("Usage: blender --background --python export_blender.py -- --input file.blend --output output.glb")
        return False
    
    # Clear existing scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Load blend file
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    
    # Select all mesh objects
    mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    
    for obj in mesh_objects:
        obj.select_set(True)
    
    # Export based on format
    if export_format == "glb":
        bpy.ops.export_scene.gltf(
            filepath=output_path,
            export_format='GLB',
            use_selection=True,
            export_materials='EXPORT',
            export_animations=True
        )
    elif export_format == "obj":
        bpy.ops.export_scene.obj(
            filepath=output_path,
            use_selection=True
        )
    else:
        print(f"Unsupported format: {export_format}")
        return False
    
    print(f"Exported {len(mesh_objects)} objects to {output_path}")
    return True

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Export Blender assets")
    
    # Blender passes its own args, we need to ignore them
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]
    else:
        argv = []
    
    parser.add_argument("--input", required=True, help="Input .blend file")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--format", default="glb", choices=["glb", "obj"], help="Export format")
    
    return parser.parse_args(argv)

if __name__ == "__main__":
    args = parse_args()
    success = export_blender_assets(args.input, args.output, args.format)
    sys.exit(0 if success else 1)