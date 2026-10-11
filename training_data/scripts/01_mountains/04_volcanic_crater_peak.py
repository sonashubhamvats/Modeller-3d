"""Dark conical volcanic peak with a visible crater basin and glowing orange lava."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
ash = mat("Ash-black rock", (0.055, 0.06, 0.065), 0.9)
lava = mat("Magma", (1.0, 0.08, 0.005), 0.3)
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=1.5, radius2=0.3, depth=2.3, location=(0, 0, 1.15))
mountain = bpy.context.object
mountain.name = "Volcanic cone"
mountain.data.materials.append(ash)
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.43, depth=0.08, location=(0, 0, 2.12))
pool = bpy.context.object
pool.name = "Crater lava pool"
pool.data.materials.append(lava)
bpy.ops.mesh.primitive_torus_add(major_radius=0.52, minor_radius=0.12, major_segments=12, minor_segments=6, location=(0, 0, 2.1))
bpy.context.object.data.materials.append(ash)
