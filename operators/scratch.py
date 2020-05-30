import bpy

from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import add_driver
from ..utils.constraints import *
from ..utils.objects import set_parent


from ..stefanos.circles import *
from ..stefanos.intersections import *
from ..stefanos.inversion import *
from ..stefanos.lines import *
from ..stefanos.triangle_constructions import *


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

        #(A, B) = context.selected_objects[-2:]
        A = context.active_object
        #others = [A, B]
        # others.remove(A)
        #B = others[0]

        #inverted_circle = new_circle()
        #center = new_empty()
        #inversion_cicle_not_on(inverted_circle, center, B, A)
        # inter1=new_empty()
        # inter2=new_empty()
        #line_circle_intersections(inter1, inter2, A, B)

        c = new_empty()
        copy_location(c, A)
        c.name = "AAAAAAAAAAAAAAA"
        '''
        line2 = new_line()
        move_origin_center(line2, center='MEDIAN')
        # Make the line really large to ensure it encompasses the circle
        line2.scale.x = 100
        copy_transforms(line2, A, transforms='LR')

        pr_cyl = new_cylinder(vert=1000)
        copy_transforms(pr_cyl, B, transforms='LR')
        copy_scale(pr_cyl, target=B, axes='XY')  # Don't copy Z scale

        inter_1 = new_empty()
        position_on_curve(inter_1, line2, position=0)
        copy_rotation(inter_1, line2)
        #project_along_axis(inter_1, 'X', target=pr_cyl, opposite=True)
        #copy_rotation(inter_1, circle)
        inter_1.name = "Intersection 1"

        inter_2 = new_empty()
        position_on_curve(inter_2, line2, position=1)
        copy_rotation(inter_2, line2)
        #project_along_axis(inter_2, 'X', target=pr_cyl, opposite=True)
        #copy_rotation(inter_2, circle)
        inter_2.name = "Intersection 2"
        '''

        return {'FINISHED'}
