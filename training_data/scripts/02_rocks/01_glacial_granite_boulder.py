"""Asymmetric rounded medium-grey granite boulder with a flattened resting base."""
import bpy


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
stone = bpy.data.materials.new("Glacial granite")
stone.diffuse_color = (0.42, 0.45, 0.47, 1)
stone.roughness = 0.75
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(0, 0, 0.68))
rock = bpy.context.object
rock.name = "Rounded granite boulder"
rock.scale = (1.0, 0.82, 0.68)
rock.data.materials.append(stone)
for vertex in rock.data.vertices:
    vertex.co.x *= 1 + 0.08 * vertex.co.y
