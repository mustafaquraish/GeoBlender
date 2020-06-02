import bpy

from GeoBlender.utils.objects import new_plane
from GeoBlender.utils.objects import new_point
from GeoBlender.utils.objects import new_line
from GeoBlender.geometry.core import make_orthogonal_to
from GeoBlender.utils.constraints import copy_location
from GeoBlender.utils.constraints import copy_rotation
from GeoBlender.utils.constraints import project_nearest
from GeoBlender.utils.constraints import locked_track
from GeoBlender.geometry.lines import bisecting_line_of_points
from GeoBlender.geometry.intersections import line_line_inteserction



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

        others = context.selected_objects[-3:]
        A = context.active_object
        others.remove(A)
        (B,C) = others

        perp1 = new_line(length=100)
        perp2 = new_line(length=30)
        perp1.name = "perp. bisector 1"
        perp2.name = "perp. bisector 2"
        bisecting_line_of_points(perp1, A, B)
        bisecting_line_of_points(perp2, A, C)
        point = new_point()
        line_line_inteserction(
        inter=point,
        line1=perp1,
        line2=perp2,
        hide_extra=False
        )

          

        

        return {'FINISHED'}





