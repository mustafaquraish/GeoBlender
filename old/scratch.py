import bpy

from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import add_driver
from ..utils.constraints import *

from ..geometry.lines import *
from ..geometry.circles import *
from ..geometry.intersections import *
from ..geometry.planes import *
from ..geometry.core import *

# from ..stefanos.circles import *
# from ..stefanos.intersections import *
# from ..stefanos.inversion import *
# from ..stefanos.lines import *
# from ..stefanos.triangle_constructions import *


class Scratch(bpy.types.Operator):
    bl_label = "Scratch Operator"
    bl_idname = "geometry.scratch_test"
    bl_description = "Add an empty in the middle of objects"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = 'Triangle Constructions > New sub Panel'

    hide: bpy.props.BoolProperty(
        name="Hide:",
        description="hide",
        default=True,
    )

    def execute(self, context):

        (A, B) = context.selected_objects[-2:]
        #A = context.active_object
        #others = [A, line]
        # others.remove(A)
        #line = others[0]

        circ = new_circle()
        circle_from_diameter(circ, A, B)

        return {'FINISHED'}
