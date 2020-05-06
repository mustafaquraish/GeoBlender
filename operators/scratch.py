import bpy
from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import *
from ..utils.constraints import *


class Scratch(bpy.types.Operator):
    bl_label = "Scratch Operator"
    bl_idname = "geometry.scratch_test"
    bl_description = "Add an empty in the middle of objects"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide: bpy.props.BoolProperty(
        name="Hide:",
        description="hide",
        default=True,
    )

    def execute(self, context):

        if (len(context.selected_objects) != 3):
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]

        empty = new_empty()
        put_at_incenter(empty, A, B, C, hide_extra=self.hide)

        return {'FINISHED'}
