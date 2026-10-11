"""Winding garden pathway of individual rounded grey cobbles embedded in dark soil."""
import bpy
import random


random.seed(23)
def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.85
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
soil = mat("Pathway dirt", (0.15, 0.11, 0.09))
stone = mat("Slate cobbles", (0.32, 0.33, 0.34))
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
base = bpy.context.object
base.name = "Soil path base"
base.dimensions = (2.4, 1.1, 0.12)
base.data.materials.append(soil)
for i in range(18):
    x = -1.0 + i * 0.12
    y = 0.28 * __import__("math").sin(i * 0.65)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.18, 0.25), location=(x, y, 0.11))
    cobble = bpy.context.object
    cobble.name = "Rounded cobblestone"
    cobble.scale.z = 0.42
    cobble.data.materials.append(stone)
