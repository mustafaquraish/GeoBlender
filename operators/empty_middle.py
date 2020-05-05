import bpy
from ..utils.objects import new_empty
from ..utils.geometry import put_in_between


class EmptyMiddle(bpy.types.Operator):
    bl_label = "Empty between objects"
    bl_idname = "geometry.empty_middle"
    bl_description = "Add an empty in the middle of objects"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    influence: bpy.props.FloatProperty(
        name="Position:",
        description="Influence",
        max=1.0,
        min=0.0,
        default=0.5,
        options={'SKIP_SAVE'},
    )

    def execute(self, context):

        if (len(context.selected_objects) != 2):
            self.report({'ERROR'}, 'Need to select 2 objects')
            return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]

        empty = new_empty()
        put_in_between(empty, A, B, influence=self.influence)

        return {'FINISHED'}
