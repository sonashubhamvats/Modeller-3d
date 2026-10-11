"""Tall narrow grey-green limestone karst pillar with vertical erosion grooves and base moss."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
stone = mat("Mossy limestone", (0.32, 0.39, 0.32), 0.85)
moss = mat("Dark moss", (0.08, 0.19, 0.09), 0.95)
bpy.ops.mesh.primitive_cone_add(vertices=9, radius1=0.72, radius2=0.32, depth=3.2, location=(0, 0, 1.6))
pillar = bpy.context.object
pillar.name = "Karst pinnacle"
pillar.data.materials.append(stone)
for x, y, scale in [(-0.42, 0.0, 0.35), (0.32, 0.22, 0.28), (0.05, -0.48, 0.3)]:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=scale, location=(x, y, scale * 0.6))
    bpy.context.object.data.materials.append(moss)
