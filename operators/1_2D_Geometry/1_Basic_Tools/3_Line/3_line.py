import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel
from GeoBlender.geometry.lines import line


class Line(bpy.types.Operator):
    bl_label = "Line"
    bl_idname = "geometry.line"
    bl_description = "Add a line through 2 points. Select two points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of line",
        min=0,
        soft_max=300,
        default=100,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        newline = new_line()
        line(newline, A, B, length=self.length)
        add_abs_bevel(newline, self.bevel_depth)
        newline.name = "Line"

        return {'FINISHED'}
