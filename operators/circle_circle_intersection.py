import bpy
from ..utils.objects import new_point
from ..geometry.intersections import circle_circle_intersection


class CircleCircleIntersection(bpy.types.Operator):
    bl_label = "Circle-Circle Intersection"
    bl_idname = "geometry.circle_circle_intersection"
    bl_description = "Place a line at the intersection of 2 circles"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = 'Planar Intersections'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for orthocenter",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        # return False
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) and
                isinstance(B.data, bpy.types.Curve)):
            return False

        if 'Circle' not in A.data.name or 'Circle' not in B.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        (A, B) = context.selected_objects[-2:]

        X = new_point()
        Y = new_point()
        circle_circle_intersection(X, Y, A, B, hide_extra=self.hide_extra)

        return {'FINISHED'}
