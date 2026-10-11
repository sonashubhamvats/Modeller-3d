"""Small arched oak footbridge with plank deck, wooden rails and dark iron fasteners."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
oak = mat("Oak bridge wood", (0.48, 0.27, 0.11), 0.7)
iron = mat("Dark iron rivets", (0.055, 0.06, 0.065), 0.45)
for i in range(9):
    x = -1.0 + i * 0.25
    z = 0.38 + 0.3 * (1 - (x / 1.15) ** 2)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, z))
    plank = bpy.context.object
    plank.name = "Oak deck plank"
    plank.dimensions = (0.23, 0.9, 0.12)
    plank.data.materials.append(oak)
for y in (-0.42, 0.42):
    for x in (-0.9, 0, 0.9):
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=0.7, location=(x, y, 0.72))
        post = bpy.context.object
        post.name = "Bridge post"
        post.data.materials.append(oak)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y, 1.08))
    rail = bpy.context.object
    rail.name = "Bridge handrail"
    rail.dimensions = (2.0, 0.1, 0.1)
    rail.data.materials.append(oak)
for x in (-0.9, -0.45, 0, 0.45, 0.9):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=4, radius=0.035, location=(x, -0.16, 0.5 + 0.3 * (1 - (x / 1.15) ** 2)))
    bpy.context.object.name = "Iron fastener"
    bpy.context.object.data.materials.append(iron)
