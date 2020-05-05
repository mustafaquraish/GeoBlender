import bpy
from ..utils.objects import new_line
from ..utils.geometry import stretch_between_points


class LineBetweenPoints(bpy.types.Operator):
    bl_label = "Line Between Points"
    bl_idname = "geometry.line_between_points"
    bl_description = "Make a line connecting two points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    def execute(self, context):

        if (len(context.selected_objects) != 2):
            self.report({'ERROR'}, 'Need to select 2 objects')
            return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]

        line = new_line()
        stretch_between_points(line, A, B, axis='Z')
        line.data.bevel_depth = self.bevel_depth

        return {'FINISHED'}
