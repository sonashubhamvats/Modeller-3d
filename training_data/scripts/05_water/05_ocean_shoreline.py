"""Curved coastal shoreline with blue water, pale foam bands and dark wet sand."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
sand = mat("Wet beach sand", (0.42, 0.31, 0.22), 0.65)
blue = mat("Ocean blue", (0.015, 0.25, 0.48), 0.2)
foam = mat("Sea foam", (0.68, 0.88, 0.92), 0.35)
for name, y, color_mat, scale in [
    ("Sand", -0.48, sand, (2.2, 0.95, 0.12)),
    ("Shallow water", 0.18, blue, (2.2, 0.8, 0.08)),
]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y, 0))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    obj.data.materials.append(color_mat)
for y, width in [(0.0, 1.7), (0.1, 1.35)]:
    bpy.ops.mesh.primitive_torus_add(major_radius=width, minor_radius=0.045, major_segments=32, minor_segments=5, location=(0, y, 0.08))
    band = bpy.context.object
    band.name = "Curved foam crest"
    band.scale.y = 0.28
    band.data.materials.append(foam)
