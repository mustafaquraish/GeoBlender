import bpy
from ..utils.objects import new_point
from ..geometry.lines import reflect_across_line

class ReflectAboutLine(bpy.types.Operator):
    bl_label = "Reflect about line"
    bl_idname = "geometry.reflect_about_line"
    bl_description = "Reflect an object about a line"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '3D Constructions'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for reflection",
        default=True,
    )


    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]
        active = bpy.context.object

        others = [A, B]
        others.remove(active)
        other = others[0]

        # active, other

        empty = new_point()
        reflect_across_line(empty, active, other, hide_extra=self.hide_extra)
        return {'FINISHED'}
