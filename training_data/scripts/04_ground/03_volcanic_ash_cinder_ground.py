"""Matte black ash patch with porous dark cinders and subtle rusty-red mineral flecks."""
import bpy
import random


random.seed(9)
def mat(name, color, roughness=0.98):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
ash = mat("Black volcanic ash", (0.07, 0.07, 0.065))
cinder = mat("Scoria", (0.16, 0.15, 0.14))
oxide = mat("Iron oxide", (0.42, 0.09, 0.025))
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
ground = bpy.context.object
ground.name = "Ash ground patch"
ground.dimensions = (2.5, 2, 0.14)
ground.data.materials.append(ash)
for i in range(12):
    x, y, z = random.uniform(-1, 1), random.uniform(-0.8, 0.8), random.uniform(0.18, 0.32)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.12, 0.28), location=(x, y, z))
    rock = bpy.context.object
    rock.name = "Porous cinder"
    rock.scale = (1, 0.8, 0.75)
    rock.data.materials.append(cinder)
    if i % 4 == 0:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=4, radius=0.07, location=(x, y - 0.16, z + 0.12))
        bpy.context.object.data.materials.append(oxide)
