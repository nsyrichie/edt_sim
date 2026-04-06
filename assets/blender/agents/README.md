# Blender Agent Files

Place .blend files with rigged characters here.

## File Naming Convention
- `agent_{type}_v{version}.blend`
- Example: `agent_humanoid_v1.blend`, `agent_quadruped_v2.blend`

## Requirements
- Include armature and mesh in same file
- Use descriptive bone names
- Apply scale and rotation before export
- Keep polygon count under 50k for performance

## Structure
Each agent .blend should contain:
- Mesh object with proper UV mapping
- Armature with named bones
- Vertex groups matching bone names
- Optional: animations in NLA tracks