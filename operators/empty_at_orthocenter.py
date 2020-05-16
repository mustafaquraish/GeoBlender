import bpy
from ..utils.objects import new_empty
from ..utils.geometry import put_at_orthocenter


class EmptyAtOrthocenter(bpy.types.Operator):
    bl_label = "Place Empty at Orthocenter"
    bl_idname = "geometry.empty_orthocenter"
    bl_description = "Place empty at the orthocenter of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for orthocenter",
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

        orthocenter = new_empty()
        orthocenter.name = "Orthocenter"
        put_at_orthocenter(orthocenter, A, B, C, hide_extra=self.hide_extra)

        return {'FINISHED'}
