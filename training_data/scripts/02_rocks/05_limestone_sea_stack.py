"""Pale layered limestone sea-stack cliff with wave-cut notches at its base."""
import bpy


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.85
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
limestone = mat("Cream limestone", (0.72, 0.69, 0.60))
salt = mat("Salt highlights", (0.9, 0.9, 0.84))
for z, scale in [(0.35, (0.9, 0.65, 0.35)), (0.9, (0.75, 0.58, 0.38)), (1.55, (0.62, 0.52, 0.42))]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z))
    ledge = bpy.context.object
    ledge.name = "Layered sea stack"
    ledge.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ledge.data.materials.append(limestone)
for x in (-0.35, 0.28):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, -0.34, 0.42))
    notch = bpy.context.object
    notch.name = "Wave cut notch"
    notch.dimensions = (0.32, 0.16, 0.16)
    notch.data.materials.append(salt)
