import bpy
from ..utils.objects import new_line
from ..utils.geometry import stretch_between_points


class CreateLineSegment(bpy.types.Operator):
    bl_label = "Create Line Segment"
    bl_idname = "geometry.create_line_segment"
    bl_description = "Form the line segment connecting two points"
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
        line.name = "Line Segment"

        return {'FINISHED'}
