import bpy
from ..utils.objects import new_line, add_abs_bevel
from ..geometry.circles import make_circle_tangent_lines


class CircleTangents(bpy.types.Operator):
    bl_label = "Circle Tangents"
    bl_idname = "geometry.circle_tangents"
    bl_description = "Form the tangents from a circle to a point"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for orthocenter",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Depth for tangents bevel",
        soft_min=0.0,
        soft_max=0.5,
        default=0.0,
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) or
                isinstance(B.data, bpy.types.Curve)):
            return False

        if not (A.data is not None and 'Circle' in A.data.name) and\
           not (B.data is not None and 'Circle' in B.data.name):
            return False

        return True

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        (A, B) = context.selected_objects[-2:]

        if A.data is not None and 'Circle' in A.data.name:
            circle, point = A, B
        elif B.data is not None and 'Circle' in B.data.name:
            circle, point = B, A
        else:
            self.report({'ERROR'}, 'Need to select at least one circle')
            return {'CANCELLED'}  # Shouldn't get here...

        line1 = new_line()
        line1.name = "Tangent 1 from point"
        line2 = new_line()
        line2.name = "Tangent 2 from point"

        make_circle_tangent_lines(line1, line2, circle, point)

        add_abs_bevel(line1, self.bevel_depth)
        add_abs_bevel(line2, self.bevel_depth)

        return {'FINISHED'}
