"""Short blue stream with stepped ledges, white foam streaks and dark wet river stones."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
water = mat("Aqua water", (0.0, 0.42, 0.55), 0.2)
foam = mat("White foam", (0.78, 0.9, 0.9), 0.25)
rock = mat("Wet dark rock", (0.08, 0.11, 0.11), 0.4)
for y, z in [(-0.55, 0.6), (0, 0.38), (0.55, 0.18)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y, z))
    ledge = bpy.context.object
    ledge.name = "Stepped river ledge"
    ledge.dimensions = (1.8, 0.5, 0.28)
    ledge.data.materials.append(rock)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.36))
stream = bpy.context.object
stream.name = "Flowing water"
stream.dimensions = (1.2, 1.8, 0.08)
stream.data.materials.append(water)
for x in (-0.25, 0.2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.47))
    streak = bpy.context.object
    streak.name = "Foam streak"
    streak.dimensions = (0.08, 1.6, 0.025)
    streak.data.materials.append(foam)
