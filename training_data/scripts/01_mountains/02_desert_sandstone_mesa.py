"""Stepped flat-topped desert mesa with red-orange strata and a pale sandy summit."""
import bpy


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.9
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
terracotta = mat("Red sandstone", (0.58, 0.20, 0.10))
tan = mat("Sandy cap", (0.78, 0.57, 0.30))
for name, z, scale, m in [
    ("Lower mesa", 0.55, (1.25, 1.05, 0.55), terracotta),
    ("Middle terrace", 1.25, (1.0, 0.85, 0.45), terracotta),
    ("Upper terrace", 1.85, (0.78, 0.68, 0.28), tan),
]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(m)
