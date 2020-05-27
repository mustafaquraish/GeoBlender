import bpy
from ..utils.objects import new_line, add_abs_bevel
from ..geometry.lines import make_segment


class CreateLineSegment(bpy.types.Operator):
    bl_label = "Create Line Segment"
    bl_idname = "geometry.create_line_segment"
    bl_description = "Form the line segment connecting two points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions'

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
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
        make_segment(line, A, B)
        add_abs_bevel(line, self.bevel_depth)
        line.name = "Line Segment"

        return {'FINISHED'}
