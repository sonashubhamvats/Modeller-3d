"""Stepped cream travertine hot-spring basins filled with pale turquoise water."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
stone = mat("Travertine", (0.84, 0.8, 0.66), 0.6)
water = mat("Turquoise spring water", (0.12, 0.62, 0.72), 0.12)
for x, y, size, z in [(-0.55, 0, 1.0, 0.18), (0.5, 0.12, 0.85, 0.42)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    basin = bpy.context.object
    basin.name = "Limestone hot spring rim"
    basin.dimensions = (size, size, 0.35)
    basin.data.materials.append(stone)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=size * 0.32, depth=0.04, location=(x, y, z + 0.12))
    pool = bpy.context.object
    pool.name = "Hot spring pool"
    pool.data.materials.append(water)
