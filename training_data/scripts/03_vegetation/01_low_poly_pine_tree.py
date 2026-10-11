"""Low-poly conifer with three stacked seven-sided green cone tiers and a brown trunk."""
import bpy


def mat(name, color, roughness=0.8):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
green = mat("Emerald foliage", (0.08, 0.30, 0.20))
brown = mat("Dark brown trunk", (0.20, 0.10, 0.045))
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.16, depth=2.1, location=(0, 0, 1.05))
bpy.context.object.name = "Pine trunk"
bpy.context.object.data.materials.append(brown)
for radius, depth, z in [(0.9, 1.35, 1.25), (0.68, 1.15, 2.0), (0.43, 0.95, 2.65)]:
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=radius, radius2=0.04, depth=depth, location=(0, 0, z))
    bpy.context.object.name = "Pine foliage tier"
    bpy.context.object.data.materials.append(green)
