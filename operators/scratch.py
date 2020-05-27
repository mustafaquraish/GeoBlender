import bpy

from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import add_driver
from ..utils.constraints import *
from ..stefanos.orthogonality import *


class Scratch(bpy.types.Operator):
    bl_label = "Scratch Operator"
    bl_idname = "geometry.scratch_test"
    bl_description = "Add an empty in the middle of objects"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = 'Triangle Constructions'

    hide: bpy.props.BoolProperty(
        name="Hide:",
        description="hide",
        default=True,
    )

    def execute(self, context):
        (X, Y) = context.selected_objects[-2:]
        A = context.active_object

        others = [X, Y]
        others.remove(A)
        line = others[0]

        obj = new_empty()
        orthogonal_projection(obj, A, line, hide_extra=True):

        return {'FINISHED'}
