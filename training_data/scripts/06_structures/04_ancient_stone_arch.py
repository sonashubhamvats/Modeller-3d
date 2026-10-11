"""Freestanding ancient megalithic granite arch with a clear opening and green lichen."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
granite = mat("Aged granite", (0.24, 0.30, 0.34), 0.8)
lichen = mat("Pale green lichen", (0.43, 0.5, 0.25), 0.95)
for location, dims in [((-0.75, 0, 1.25), (0.55, 0.65, 2.5)), ((0.75, 0, 1.25), (0.55, 0.65, 2.5)), ((0, 0, 2.55), (2.05, 0.72, 0.55))]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    block = bpy.context.object
    block.name = "Megalith block"
    block.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    block.data.materials.append(granite)
for x, z in [(-0.72, 0.5), (0.74, 1.1), (0.2, 2.83)]:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.2, location=(x, -0.38, z))
    bpy.context.object.name = "Lichen patch"
    bpy.context.object.scale = (1.2, 0.3, 0.7)
    bpy.context.object.data.materials.append(lichen)
