import bpy
from ..utils.objects import new_line, add_abs_bevel, uniform_scale
from ..geometry.circles import polar_line, polar_intersection


class CircleTangent(bpy.types.Operator):
    bl_label = "Circle Polar Line"
    bl_idname = "geometry.circle_pline"
    bl_description = "Form the Polar Line for a circle and a point"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for Polar Line",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Depth for polar line bevel",
        soft_min=0.0,
        soft_max=0.5,
        default=0.0,
    )

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of line",
        soft_min=0.1,
        soft_max=1000,
        default=100,
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

        line = new_line()
        line.name = "Polar Line"
        polar_line(line, point, circle)
        add_abs_bevel(line, self.bevel_depth)
        uniform_scale(line, self.length)

        return {'FINISHED'}
