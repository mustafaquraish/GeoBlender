import bpy
from ..utils.objects import new_line, move_origin_center
from ..utils.constraints import copy_rotation, locked_track
from ..utils.geometry import put_at_radical_intercept


class CreateRadicalAxis(bpy.types.Operator):
    bl_label = "Create Radical Axis"
    bl_idname = "geometry.create_radical_axis"
    bl_description = "Form the radical axis of 2 circles"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of line",
        min=0,
        soft_max=100,
        default=30,
    )

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):

        if (len(context.selected_objects) != 2):
            self.report({'ERROR'}, 'Need to select 2 objects')
            return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) and
                isinstance(B.data, bpy.types.Curve)):
            self.report({'ERROR'}, 'Both objects needs to be curves')
            return {'CANCELLED'}

        if 'Circle' not in A.data.name or 'Circle' not in B.data.name:
            self.report({'ERROR'}, 'Need to select 2 circles')
            return {'CANCELLED'}

        radical_axis = new_line(length=self.length, axis='Y')
        move_origin_center(radical_axis)
        put_at_radical_intercept(radical_axis, A, B)
        copy_rotation(radical_axis, target=A)
        locked_track(radical_axis, lock='Z', axis='X', target=B)
        radical_axis.data.bevel_depth = self.bevel_depth
        radical_axis.name = "Radical Axis"

        return {'FINISHED'}
