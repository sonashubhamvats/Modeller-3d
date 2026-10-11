"""Ridge of staggered hexagonal charcoal basalt columns with chiseled tops."""
import bpy
import random


random.seed(11)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
stone = bpy.data.materials.new("Charcoal basalt")
stone.diffuse_color = (0.09, 0.10, 0.11, 1)
stone.roughness = 0.7
for row in range(3):
    for col in range(5):
        height = random.uniform(1.0, 2.6)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, radius=random.uniform(0.28, 0.38), depth=height,
            location=(col * 0.62 - 1.24, row * 0.58 - 0.58, height / 2),
        )
        obj = bpy.context.object
        obj.name = "Basalt column"
        obj.rotation_euler[2] = random.uniform(-0.15, 0.15)
        obj.data.materials.append(stone)
