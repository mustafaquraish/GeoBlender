import bpy
from ..utils.objects import new_empty
from ..utils.geometry import put_at_incenter


class EmptyAtIncenter(bpy.types.Operator):
    bl_label = "Place Empty at Incenter"
    bl_idname = "geometry.empty_incenter"
    bl_description = "Place empty at the incenter of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel type
    gb_panel = 'Triangle Constructions'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for incenter",
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

        incenter = new_empty()
        incenter.name = "Incenter"
        put_at_incenter(incenter, A, B, C, hide_extra=self.hide_extra)

        return {'FINISHED'}
