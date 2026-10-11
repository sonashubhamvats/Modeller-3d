"""Warm golden low-poly sand dune with an undulating crest and subtle wind-ripple ridges."""
import bpy


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.8
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
sand = mat("Golden dune sand", (0.75, 0.61, 0.38))
ridge = mat("Sunlit ripple", (0.84, 0.72, 0.5))
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=1, location=(0, 0, 0.15))
dune = bpy.context.object
dune.name = "Undulating sand dune"
dune.scale = (1.6, 1.0, 0.48)
dune.data.materials.append(sand)
for i in range(7):
    y = -0.6 + i * 0.18
    bpy.ops.mesh.primitive_torus_add(major_radius=0.62 - abs(y) * 0.28, minor_radius=0.018, major_segments=24, minor_segments=4, location=(0, y, 0.39 - abs(y) * 0.22))
    bpy.context.object.name = "Wind ripple"
    bpy.context.object.data.materials.append(ridge)
