import bpy
from ..utils.objects import new_point
from ..geometry.intersections import line_circle_intersections


class LineCircleIntersection(bpy.types.Operator):
    bl_label = "Line-Circle Intersection"
    bl_idname = "geometry.line_circle_intersection"
    bl_description = "Place empty at the intersection of 2 a line " +\
                     "and circle on the same plane"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    gb_panel = 'Planar Intersections'  # GeoBlender Panel for the operator

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for orthocenter",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) and
                isinstance(B.data, bpy.types.Curve)):
            return False

        if (not ('Circle' in A.data.name and 'Line' in B.data.name) and
                not ('Line' in A.data.name and 'Circle' in B.data.name)):
            return False

        return True

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        if 'Circle' in A.data.name and 'Line' in B.data.name:
            circle, line = A, B
        elif 'Line' in A.data.name and 'Circle' in B.data.name:
            circle, line = B, A
        else:
            self.report({'ERROR'}, 'Need to select a line and a circle')
            return {'CANCELLED'}  # Shouldn't get here...

        (A, B) = context.selected_objects[-2:]

        X = new_point()
        Y = new_point()
        line_circle_intersections(
            X, Y, line, circle, hide_extra=self.hide_extra)

        return {'FINISHED'}
