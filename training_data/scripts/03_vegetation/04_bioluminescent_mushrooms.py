"""Three fantasy mushrooms with cream stalks, cyan luminous-looking caps and gill undersides."""
import bpy


def mat(name, color, roughness=0.5):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
cream = mat("Pale stalks", (0.86, 0.82, 0.68))
cyan = mat("Cyan caps", (0.0, 0.65, 0.78), 0.25)
gill = mat("Glowing gills", (0.45, 0.9, 0.95), 0.3)
moss = mat("Moss base", (0.08, 0.24, 0.1))
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.75, depth=0.18, location=(0, 0, 0.09))
bpy.context.object.data.materials.append(moss)
for x, y, height, radius in [(-0.45, 0, 1.0, 0.5), (0.38, 0.05, 1.4, 0.62), (0, 0.42, 0.8, 0.38)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.13, depth=height, location=(x, y, height / 2 + 0.12))
    bpy.context.object.data.materials.append(cream)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=radius, location=(x, y, height + 0.18))
    cap = bpy.context.object
    cap.scale.z = 0.42
    cap.data.materials.append(cyan)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=radius * 0.65, depth=0.035, location=(x, y, height + 0.08))
    bpy.context.object.data.materials.append(gill)
