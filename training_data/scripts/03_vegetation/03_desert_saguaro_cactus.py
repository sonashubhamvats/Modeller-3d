"""Ribbed sage-green saguaro cactus with two asymmetrical raised arms and spine dots."""
import bpy


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.7
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
green = mat("Sage cactus", (0.25, 0.40, 0.25))
spines = mat("Cream spines", (0.88, 0.82, 0.65))
for loc, depth, radius in [((0, 0, 1.35), 2.7, 0.42), ((-0.53, 0, 1.8), 1.4, 0.25), ((0.56, 0, 2.2), 1.1, 0.24)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=radius, depth=depth, location=loc)
    stem = bpy.context.object
    stem.name = "Ribbed saguaro stem"
    stem.data.materials.append(green)
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.25, depth=0.9, location=(-0.7, 0, 1.7))
bpy.context.object.rotation_euler[1] = 1.35
bpy.context.object.data.materials.append(green)
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.24, depth=0.7, location=(0.73, 0, 2.1))
bpy.context.object.rotation_euler[1] = 1.35
bpy.context.object.data.materials.append(green)
for z in (0.65, 1.1, 1.55, 2.0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=4, radius=0.045, location=(0.0, -0.405, z))
    bpy.context.object.name = "Spine cluster"
    bpy.context.object.data.materials.append(spines)
