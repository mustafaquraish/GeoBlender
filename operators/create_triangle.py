import bpy
from ..utils.objects import new_line
from ..utils.geometry import stretch_between_points


class CreateTriangle(bpy.types.Operator):
    bl_label = "Create Triangle"
    bl_idname = "geometry.create_triangle"
    bl_description = "Form the triangle of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]

        lines = [new_line(), new_line(), new_line()]
        stretch_between_points(lines[0], A, B)
        stretch_between_points(lines[1], B, C)
        stretch_between_points(lines[2], C, A)
        for idx, line in enumerate(lines):
            line.name = f"Side {idx + 1}"
            line.data.bevel_depth = self.bevel_depth

        # TODO: Figure out how to join the lines without breaking the bevel.

        return {'FINISHED'}
