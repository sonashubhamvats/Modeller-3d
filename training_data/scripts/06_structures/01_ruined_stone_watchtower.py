"""Broken cylindrical grey masonry watchtower with missing top stones and climbing green ivy."""
import bpy


def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = 0.85
    return m


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
stone = mat("Weathered masonry", (0.36, 0.39, 0.42))
ivy = mat("Green ivy", (0.08, 0.25, 0.09))
for z, radius in [(0.35, 0.75), (0.85, 0.68), (1.35, 0.62), (1.85, 0.58)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=radius, depth=0.48, location=(0, 0, z))
    course = bpy.context.object
    course.name = "Stone tower course"
    course.data.materials.append(stone)
for x, z in [(-0.4, 0.9), (0.32, 1.5), (0.0, 1.9)]:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.2, location=(x, -0.55, z))
    bpy.context.object.name = "Ivy cluster"
    bpy.context.object.data.materials.append(ivy)
