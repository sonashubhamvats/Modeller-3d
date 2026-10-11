"""Uneven olive tundra soil with low grass mounds and scattered icy frost patches."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
soil = mat("Olive tundra moss", (0.34, 0.36, 0.24), 0.9)
ice = mat("Blue-white frost", (0.72, 0.82, 0.86), 0.3)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
base = bpy.context.object
base.name = "Frozen ground"
base.dimensions = (2.3, 1.9, 0.2)
base.data.materials.append(soil)
for x, y, scale in [(-0.7, -0.35, 0.38), (0.1, 0.25, 0.45), (0.72, -0.2, 0.32)]:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=scale, location=(x, y, 0.18))
    mound = bpy.context.object
    mound.name = "Tundra grass mound"
    mound.scale.z = 0.45
    mound.data.materials.append(soil)
for x, y in [(-0.65, 0.45), (0.35, -0.5), (0.75, 0.5)]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.36, location=(x, y, 0.14))
    patch = bpy.context.object
    patch.name = "Frost patch"
    patch.scale.z = 0.08
    patch.data.materials.append(ice)
