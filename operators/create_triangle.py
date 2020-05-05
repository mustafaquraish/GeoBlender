import bpy
from ..utils.objects import new_line
from ..utils.geometry import stretch_between_points


class CreateTriangle(bpy.types.Operator):
    bl_label = "Create Triangle"
    bl_idname = "geometry.create_triangle"
    bl_description = "Form the triangle of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    def execute(self, context):

        if (len(context.selected_objects) != 3):
            self.report({'ERROR'}, 'Need to select 3 objects')
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]

        lines = [new_line(), new_line(), new_line()]
        stretch_between_points(lines[0], A, B)
        stretch_between_points(lines[1], B, C)
        stretch_between_points(lines[2], C, A)
        for line in lines:
            line.data.bevel_depth = self.bevel_depth

        return {'FINISHED'}