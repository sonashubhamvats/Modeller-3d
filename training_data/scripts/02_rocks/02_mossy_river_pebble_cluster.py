"""Five smooth dark slate river pebbles with small green moss caps."""
import bpy


def mat(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
slate = mat("River slate", (0.22, 0.25, 0.26), 0.75)
moss = mat("Velvety moss", (0.07, 0.25, 0.08), 0.95)
positions = [(-0.65, 0, 0.35), (0, 0.05, 0.42), (0.62, 0, 0.32), (-0.32, 0.55, 0.28), (0.38, 0.55, 0.3)]
for i, pos in enumerate(positions):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.42, location=pos)
    pebble = bpy.context.object
    pebble.name = f"River pebble {i + 1}"
    pebble.scale = (1.0, 0.78, 0.66)
    pebble.data.materials.append(slate)
    if i % 2 == 0:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.22, location=(pos[0], pos[1], pos[2] + 0.25))
        bpy.context.object.name = "Moss cap"
        bpy.context.object.scale.z = 0.28
        bpy.context.object.data.materials.append(moss)
