"""Still algae-green swamp pool with emerging reeds, muddy islets and floating lily pads."""
import bpy


def mat(name, color, roughness=0.6):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
water = mat("Murky algae water", (0.18, 0.27, 0.1), 0.35)
leaf = mat("Lily pad green", (0.12, 0.34, 0.22), 0.8)
reed = mat("Reed stems", (0.42, 0.34, 0.12), 0.8)
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1.3, depth=0.12, location=(0, 0, 0))
bpy.context.object.name = "Swamp pool"
bpy.context.object.data.materials.append(water)
for x, y, height in [(-0.5, 0, 0.9), (0.15, 0.25, 1.2), (0.55, -0.3, 0.75), (-0.1, -0.45, 0.95)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.035, depth=height, location=(x, y, height / 2 + 0.05))
    bpy.context.object.name = "Emerging reed"
    bpy.context.object.data.materials.append(reed)
for x, y in [(-0.8, -0.3), (0.65, 0.45), (0.2, -0.7)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.25, depth=0.035, location=(x, y, 0.1))
    bpy.context.object.name = "Lily pad"
    bpy.context.object.data.materials.append(leaf)
