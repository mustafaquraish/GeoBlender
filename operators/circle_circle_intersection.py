import bpy
from ..utils.objects import new_empty, new_cylinder
from ..utils.constraints import position_on_curve, copy_transforms, damped_track, copy_location
from ..utils.geometry import put_in_between, put_at_radical_intercept
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

        (A, B) = context.selected_objects[-2:]

        int_center = new_empty(hide=self.hide_extra)
        put_at_radical_intercept(int_center, A, B)

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

        return {'FINISHED'}
