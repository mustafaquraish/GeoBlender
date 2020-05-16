import bpy
from ..utils.objects import new_empty, new_cylinder, new_line
from ..utils.constraints import position_on_curve, copy_transforms
from ..utils.constraints import locked_track, copy_rotation
from ..utils.geometry import put_in_between, stretch_between_points
from ..utils.constraints import project_along_axis, copy_location
from ..utils.drivers import add_driver_distance, add_driver, driver_namespace


class CircleTangents(bpy.types.Operator):
    bl_label = "Circle Tangents"
    bl_idname = "geometry.circle_tangents"
    bl_description = "Form the tangents from a circle to a point"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for orthocenter",
        default=True,
    )

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        if (len(context.selected_objects) != 2):
            self.report({'ERROR'}, 'Need to select 2 objects')
            return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) or
                isinstance(B.data, bpy.types.Curve)):
            self.report({'ERROR'}, 'Need to select at least one Circle')
            return {'CANCELLED'}

        if A.data is not None and 'Circle' in A.data.name:
            circle, point = A, B
        elif B.data is not None and 'Circle' in B.data.name:
            circle, point = B, A
        else:
            self.report({'ERROR'}, 'Need to select a circle and other object')
            return {'CANCELLED'}

        '''
        General idea here:
        - Have a circle C centered at point A
        - Have a point at point B
        - Let M be the midpoint of A-B
        - Consider the circle C' centered at M, with radius len(A-B)/2
        - The tangents from C to B touch the circle at the intersection
            points of the circles C' and C.
        '''

        int_center = new_empty(hide=self.hide_extra)
        add_driver(
            obj=int_center,
            prop='location',
            fields='XYZ',
            vars_def={
                'd': ('distance', circle, point),
                'r1': ('transform', circle, 'scale', 'X'),
                'o1': ('transform', A, 'location', '-'),
                'o2': ('transform', B, 'location', '-'),
            },
            # Parameters to the helper function:
            #   distance: len(A-B) / 2
            #   r1      : radius of C
            #   r2      : radius of C', len(A-B) / 2
            #   o1      : location of C, A
            #   o2      : location of M, (A + B) / 2
            expr='gb_radical_axis_intercept(d/2, r1, d/2, o1, (o1+o2)/2)'
        )

        pr_cyl = new_cylinder(hide=self.hide_extra)
        copy_transforms(pr_cyl, target=circle)

        int_1 = new_empty(hide=self.hide_extra)
        copy_location(int_1, int_center)
        copy_rotation(int_1, A)
        locked_track(int_1, lock='Z', axis='X', target=B)
        project_along_axis(int_1, axis='Y', target=pr_cyl)

        int_2 = new_empty(hide=self.hide_extra)
        copy_location(int_2, int_center)
        copy_rotation(int_2, A)
        locked_track(int_2, lock='Z', axis='X', target=B)
        project_along_axis(int_2, axis='-Y', target=pr_cyl)

        tangent1 = new_line()
        stretch_between_points(tangent1, int_1, point)

        tangent2 = new_line()
        stretch_between_points(tangent2, int_2, point)

        return {'FINISHED'}
