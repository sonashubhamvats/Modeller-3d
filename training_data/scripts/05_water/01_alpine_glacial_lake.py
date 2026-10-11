"""Recessed teal alpine glacial lake surrounded by a rough ring of mountain rocks."""
import bpy
import random


random.seed(7)
def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
rock = mat("Rocky shore", (0.28, 0.31, 0.32), 0.85)
water = mat("Glacial teal water", (0.01, 0.28, 0.34), 0.08)
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1.3, depth=0.18, location=(0, 0, 0))
shore = bpy.context.object
shore.name = "Lake shore base"
shore.data.materials.append(rock)
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.82, depth=0.035, location=(0, 0, 0.04))
pool = bpy.context.object
pool.name = "Recessed glacial lake"
pool.data.materials.append(water)
for i in range(14):
    angle = i * 6.283 / 14
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.12, 0.22), location=(1.05 * __import__("math").cos(angle), 1.05 * __import__("math").sin(angle), 0.12))
    bpy.context.object.name = "Shore rock"
    bpy.context.object.data.materials.append(rock)
