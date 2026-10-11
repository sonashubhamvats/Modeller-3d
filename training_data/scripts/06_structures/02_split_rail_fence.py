"""Short rustic split-rail wooden fence with rough rails following a gentle slope."""
import bpy


wood = bpy.data.materials.new("Weathered timber")
wood.diffuse_color = (0.25, 0.14, 0.09, 1)
wood.roughness = 0.9
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for x, z in [(-1, 0.55), (0, 0.75), (1, 0.95)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.11, depth=1.1, location=(x, 0, z))
    post = bpy.context.object
    post.name = "Fence post"
    post.data.materials.append(wood)
for z in (0.55, 1.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z + 0.08))
    rail = bpy.context.object
    rail.name = "Split rail"
    rail.dimensions = (2.25, 0.12, 0.13)
    rail.rotation_euler[1] = 0.18
    rail.data.materials.append(wood)
