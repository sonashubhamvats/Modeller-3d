"""Twisted brown oak trunk with branching limbs and rounded amber-orange autumn canopy."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bark = mat("Ridged dark bark", (0.18, 0.075, 0.035), 0.95)
leaves = mat("Autumn amber", (0.72, 0.25, 0.055), 0.8)
bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=0.34, radius2=0.17, depth=2.3, location=(0, 0, 1.15))
bpy.context.object.name = "Oak trunk"
bpy.context.object.data.materials.append(bark)
for x, angle in [(-0.55, -0.55), (0.5, 0.55), (-0.2, 0.2), (0.25, -0.2)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=7, radius=0.11, depth=1.35, location=(x * 0.5, 0, 2.05))
    branch = bpy.context.object
    branch.name = "Oak branch"
    branch.rotation_euler[1] = angle
    branch.data.materials.append(bark)
for x, y, z, radius in [(-0.8, 0, 2.7, 0.62), (0, 0, 3.0, 0.72), (0.75, 0, 2.65, 0.6), (0, 0.4, 2.65, 0.55)]:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=(x, y, z))
    bpy.context.object.name = "Autumn foliage cluster"
    bpy.context.object.data.materials.append(leaves)
