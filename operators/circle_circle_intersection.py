import bpy
from ..utils.objects import new_empty, new_cylinder
from ..utils.constraints import position_on_curve, copy_transforms, damped_track, copy_location
from ..utils.geometry import put_in_between
from ..utils.constraints import project_along_axis, copy_rotation, locked_track
from ..utils.drivers import add_driver_distance, add_driver, driver_namespace


class CircleCircleIntersection(bpy.types.Operator):
    bl_label = "Circle-Circle Intersection"
    bl_idname = "geometry.circle_circle_intersection"
    bl_description = "Place a line at the intersection of 2 circles"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for orthocenter",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        # return False
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) and
                isinstance(B.data, bpy.types.Curve)):
            return False

        if 'Circle' not in A.data.name or 'Circle' not in B.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        # if (len(context.selected_objects) != 2):
        #     self.report({'ERROR'}, 'Need to select 2 objects')
        #     return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]

        # if not (isinstance(A.data, bpy.types.Curve) and
        #         isinstance(B.data, bpy.types.Curve)):
        #     self.report({'ERROR'}, 'Both objects needs to be curves')
        #     return {'CANCELLED'}

        # if 'Circle' not in A.data.name or 'Circle' not in B.data.name:
        #     self.report({'ERROR'}, 'Need to select 2 circles')
        #     return {'CANCELLED'}

        int_center = new_empty(hide=self.hide_extra)
        add_driver(
            obj=int_center,
            prop='location',
            fields='XYZ',
            vars_def={
                'd': ('distance', A, B),
                'r1': ('transform', A, 'scale', 'X'),
                'r2': ('transform', B, 'scale', 'X'),
                'o1': ('transform', A, 'location', '-'),
                'o2': ('transform', B, 'location', '-'),
            },
            expr='gb_radical_axis_intercept(d, r1, r2, o1, o2)'
        )

        pr_cyl = new_cylinder(hide=self.hide_extra)
        copy_transforms(pr_cyl, target=A)

        int_1 = new_empty()
        copy_location(int_1, int_center)
        copy_rotation(int_1, A)
        locked_track(int_1, lock='Z', axis='X', target=B)
        project_along_axis(int_1, axis='Y', target=pr_cyl)

        int_2 = new_empty()
        copy_location(int_2, int_center)
        copy_rotation(int_2, A)
        locked_track(int_2, lock='Z', axis='X', target=B)
        project_along_axis(int_2, axis='-Y', target=pr_cyl)

        # line = new_line()
        # move_origin_center(line)
        # put_in_between(line, int_1, int_2, influence=0.5)
        # damped_track(line, axis="Z", target=int_1)
        # add_driver_distance(line, 'scale', 'Z', int_1, int_2, 100)
        # line.name = "Line"

        return {'FINISHED'}
