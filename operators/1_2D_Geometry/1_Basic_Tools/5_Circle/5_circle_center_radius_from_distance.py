import bpy
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.geometry.circles import circle_from_center_distance


class CircleCenterRadius(bpy.types.Operator):
    bl_label = "Circle through center and distance"
    bl_idname = "geometry.circle_center_distance"
    bl_description = (
        "Add a circle with given center and radius equal to "
        "the distance of two points. Select three points. "
        "The center should be the active object. The distance of "
        "the other two points determine the radius")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.2,
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

        circle = new_circle()
        circle_from_center_distance(circle, A, X, Y)
        add_abs_bevel(circle, self.bevel_depth)

        return {'FINISHED'}
