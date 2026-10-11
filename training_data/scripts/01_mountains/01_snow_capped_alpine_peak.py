"""Low-poly alpine summit: sharp faceted grey granite cliffs with a bright snow cap."""
import bpy


def material(name, color, roughness=0.8):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.roughness = roughness
    return mat


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
rock = material("Granite", (0.24, 0.25, 0.27), 0.8)
snow = material("Snow", (0.82, 0.88, 0.94), 0.4)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(0, 0, 1))
peak = bpy.context.object
peak.name = "Angular alpine peak"
peak.scale = (1.25, 1.1, 1.9)
peak.data.materials.append(rock)
bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=1.0, radius2=0.08, depth=1.15, location=(0, 0, 2.5))
cap = bpy.context.object
cap.name = "Snow cap"
cap.data.materials.append(snow)
