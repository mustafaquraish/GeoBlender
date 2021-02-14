import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel
from GeoBlender.geometry.lines_3d import segment


class Segment(bpy.types.Operator):
    bl_label = "Segment"
    bl_idname = "geometry.3d_segment"
    bl_description = "Add a segment between 2 points. Select two points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of segment",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        line = new_line()
        segment(line, A, B)
        add_abs_bevel(line, self.bevel_depth)
        line.name = "Line Segment"

        return {'FINISHED'}
