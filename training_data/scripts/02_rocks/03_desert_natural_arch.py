"""Freestanding red sandstone natural arch with visible opening and sediment bands."""
import bpy


def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.9
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
rock = material("Red sandstone", (0.55, 0.16, 0.08))
strata = material("Sandstone strata", (0.72, 0.34, 0.17))
for location, dims in [((-0.75, 0, 1), (0.55, 0.7, 2)), ((0.75, 0, 1), (0.55, 0.7, 2)), ((0, 0, 2.0), (1.9, 0.7, 0.55))]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = "Weathered arch stone"
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(rock)
for z in (0.8, 1.25, 1.7, 2.25):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.36, z))
    band = bpy.context.object
    band.name = "Sediment band"
    band.dimensions = (2.0, 0.025, 0.045)
    band.data.materials.append(strata)
