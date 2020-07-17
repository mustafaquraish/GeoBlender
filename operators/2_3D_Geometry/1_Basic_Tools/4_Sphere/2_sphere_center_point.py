import bpy
from GeoBlender.utils.objects import new_point, new_sphere, add_abs_bevel
from GeoBlender.geometry.spheres import sphere_from_center_point


class SphereCPoint(bpy.types.Operator):
    bl_label = "Sphere with center and point"
    bl_idname = "geometry.3d_sphere_center_point"
    bl_description = (
        "Add a sphere with given center and through a given point. "
        "Select two points, the center should be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    segments: bpy.props.IntProperty(
        name="Resolution:",
        description="Resolution for the Sphere",
        min=3,
        soft_max=150,
        default=64,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        sphere = new_sphere(segments=self.segments)
        sphere_from_center_point(sphere, A, B)

        return {'FINISHED'}
