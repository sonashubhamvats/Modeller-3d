"""Cluster of glossy jet-black angular obsidian crystals rising from a rocky base."""
import bpy


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
glass_rock = bpy.data.materials.new("Polished obsidian")
glass_rock.diffuse_color = (0.015, 0.018, 0.022, 1)
glass_rock.roughness = 0.1
for i, (x, y, height) in enumerate([(-0.55, 0, 1.3), (0, 0.05, 2.0), (0.55, 0, 1.45), (-0.25, 0.4, 1.0), (0.35, 0.42, 1.15)]):
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.42, radius2=0.02, depth=height, location=(x, y, height / 2))
    crystal = bpy.context.object
    crystal.name = f"Obsidian shard {i + 1}"
    crystal.rotation_euler[1] = (i - 2) * 0.12
    crystal.data.materials.append(glass_rock)
