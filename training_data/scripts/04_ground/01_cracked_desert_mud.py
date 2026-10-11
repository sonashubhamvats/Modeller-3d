"""Tan-brown dried mud ground tile split into polygon-like plates with dark fissures."""
import bpy


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.95
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
clay = mat("Sun-baked clay", (0.56, 0.40, 0.24))
crack = mat("Deep fissures", (0.07, 0.045, 0.025))
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
base = bpy.context.object
base.name = "Cracked mud base"
base.dimensions = (2.4, 2.0, 0.12)
base.data.materials.append(crack)
for x in (-0.75, 0, 0.75):
    for y in (-0.55, 0.15, 0.75):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.1))
        plate = bpy.context.object
        plate.name = "Raised clay plate"
        plate.dimensions = (0.66, 0.57, 0.08)
        plate.rotation_euler[2] = (x + y) * 0.12
        plate.data.materials.append(clay)
