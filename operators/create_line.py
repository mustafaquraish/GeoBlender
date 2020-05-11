import bpy
from ..utils.objects import new_line, move_origin_center
from ..utils.geometry import put_in_between
from ..utils.constraints import damped_track


class CreateLine(bpy.types.Operator):
    bl_label = "Create Line Through Points"
    bl_idname = "geometry.create_line"
    bl_description = "Form the line going through the 2 points"
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

        line = new_line()
        move_origin_center(line)
        put_in_between(line, A, B, influence=0.5)
        damped_track(line, axis="Z", target=A)
        line.scale.z = self.length
        line.data.bevel_depth = self.bevel_depth
        line.name = "Line"

        return {'FINISHED'}
