"""Weeping willow with a leaning dark trunk and curtain-like muted green hanging foliage."""
import bpy


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.85
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bark = mat("Weathered bark", (0.15, 0.075, 0.03))
leaf = mat("Willow green", (0.42, 0.62, 0.42))
bpy.ops.mesh.primitive_cone_add(vertices=9, radius1=0.28, radius2=0.16, depth=2.5, location=(-0.15, 0, 1.25))
trunk = bpy.context.object
trunk.name = "Leaning willow trunk"
trunk.rotation_euler[1] = -0.18
trunk.data.materials.append(bark)
for x in (-0.9, -0.45, 0, 0.45, 0.9):
    bpy.ops.mesh.primitive_cylinder_add(vertices=7, radius=0.07, depth=1.5, location=(x * 0.7, 0, 2.2))
    branch = bpy.context.object
    branch.name = "Willow branch"
    branch.rotation_euler[1] = x * 0.25
    branch.data.materials.append(bark)
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=0.22, radius2=0.04, depth=1.8, location=(x, 0, 1.45))
    curtain = bpy.context.object
    curtain.name = "Hanging foliage curtain"
    curtain.data.materials.append(leaf)
