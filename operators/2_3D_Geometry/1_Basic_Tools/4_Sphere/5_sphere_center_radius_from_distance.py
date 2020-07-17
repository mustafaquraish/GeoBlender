import bpy
from GeoBlender.utils.objects import new_point, new_sphere
from GeoBlender.geometry.spheres import sphere_from_center_distance


class SphereCenterRadius(bpy.types.Operator):
    bl_label = "Sphere through center and distance"
    bl_idname = "geometry.sphere_center_distance"
    bl_description = (
        "Add a sphere with given center and radius equal to "
        "the distance of two points. Select three points. "
        "The center should be the active object. The distance of "
        "the other two points determine the radius")
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
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra

        return self.execute(context)

    def execute(self, context):

        A = context.active_object

        others = context.selected_objects[-3:]
        others.remove(A)
        (X, Y) = others

        sphere = new_sphere(segments=self.segments)
        sphere_from_center_distance(sphere, A, X, Y)

        return {'FINISHED'}
