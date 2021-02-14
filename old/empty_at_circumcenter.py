import bpy
from ..utils.objects import new_empty
from ..utils.geometry import put_at_circumcenter


class EmptyAtCircumcenter(bpy.types.Operator):
    bl_label = "Place Empty at Circumcenter"
    bl_idname = "geometry.empty_circumcenter"
    bl_description = "Place empty at the circumcenter of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = 'Triangle Constructions'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for circumcenter",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]

        circumcenter = new_empty()
        circumcenter.name = "Circumcenter"
        put_at_circumcenter(circumcenter, A, B, C, hide_extra=self.hide_extra)

        return {'FINISHED'}
