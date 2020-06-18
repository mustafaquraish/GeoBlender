import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel
from GeoBlender.geometry.lines import segment


class CreateTriangle(bpy.types.Operator):
    bl_label = "Create Triangle"
    bl_idname = "geometry.create_triangle"
    bl_description = "Form the triangle of the 3 points. Select 3 points."
    bl_options = {'REGISTER', 'UNDO'}

    # GeoBlender Panel Type
    gb_panel = 'Triangle Constructions'

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
        segment(lines[0], A, B)
        segment(lines[1], B, C)
        segment(lines[2], C, A)

        for idx, line in enumerate(lines):
            line.name = f"Side {idx + 1}"
            add_abs_bevel(line, self.bevel_depth)

        return {'FINISHED'}
