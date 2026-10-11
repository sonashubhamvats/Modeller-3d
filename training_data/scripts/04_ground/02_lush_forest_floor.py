"""Forest floor diorama with dark soil, green moss mounds, stones and pine-needle details."""
import bpy
import random


random.seed(5)
def mat(name, color, roughness=0.9):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
soil = mat("Dark loam", (0.12, 0.075, 0.035))
moss = mat("Forest moss", (0.12, 0.34, 0.2))
stone = mat("Small stones", (0.28, 0.30, 0.29))
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1.25, depth=0.18, location=(0, 0, 0))
bpy.context.object.data.materials.append(soil)
for i in range(7):
    x, y = random.uniform(-0.8, 0.8), random.uniform(-0.75, 0.75)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.22, 0.38), location=(x, y, 0.2))
    bpy.context.object.name = "Moss mound"
    bpy.context.object.scale.z = 0.55
    bpy.context.object.data.materials.append(moss)
for i in range(8):
    x, y = random.uniform(-1, 1), random.uniform(-0.9, 0.9)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.12, location=(x, y, 0.16))
    bpy.context.object.name = "Forest stone"
    bpy.context.object.data.materials.append(stone)
