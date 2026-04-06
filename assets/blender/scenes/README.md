# Blender Scene Files

Place environment .blend files here.

## File Naming Convention
- `scene_{name}_v{version}.blend`
- Example: `scene_warehouse_v1.blend`, `scene_forest_v2.blend`

## Scene Requirements
- Include collision geometry (can be simplified)
- Proper scale (1 unit = 1 meter)
- Origin at ground level
- No unnecessary objects

## Optimization Tips
- Use linked duplicates for repeated objects
- Bake lighting where possible
- Remove backfaces for collision meshes