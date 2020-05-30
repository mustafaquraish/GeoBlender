import bpy
from ..utils.objects import new_empty
from ..utils.geometry import put_in_between


class Midpoint(bpy.types.Operator):
    bl_label = "Empty between objects"
    bl_idname = "geometry.empty_middle"
    bl_description = "Add an empty in the middle of objects"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions'

    influence: bpy.props.FloatProperty(
        name="Position:",
        description="Influence",
        max=1.0,
        min=0.0,
        default=0.5,
        options={'SKIP_SAVE'},
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        empty = new_empty()
        put_in_between(empty, A, B, influence=self.influence)
        empty.name = "Midpoint"

        return {'FINISHED'}
