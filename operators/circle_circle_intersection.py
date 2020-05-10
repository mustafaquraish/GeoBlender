import bpy
from ..utils.objects import new_empty, new_cylinder, new_mesh_circle
from ..utils.constraints import position_on_curve, copy_transforms
from ..utils.constraints import project_along_axis, copy_rotation, locked_track


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

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        if (len(context.selected_objects) != 2):
            self.report({'ERROR'}, 'Need to select 2 objects')
            return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) and
                isinstance(B.data, bpy.types.Curve)):
            self.report({'ERROR'}, 'Both objects needs to be curves')
            return {'CANCELLED'}

        if 'BezierCircle' not in A.data.name or 'Circle' not in B.data.name:
            self.report({'ERROR'}, 'Need to select a line and a circle')
            return {'CANCELLED'}

        int_center = new_empty()
        copy_transforms(int_center, A, transforms='LR')
        locked_track(int_center, lock='Z', axis='X', target=B)

        mesh_circ = new_mesh_circle(hide=self.hide_extra)
        copy_transforms(mesh_circ, B)
        project_along_axis(int_center, axis='X', target=mesh_circ)

        # pr_cyl = new_cylinder(vert=100, hide=self.hide_extra)
        # copy_transforms(pr_cyl, circle)

        # intersection_1 = new_empty()
        # position_on_curve(intersection_1, line, position=0)
        # copy_rotation(intersection_1, line)
        # project_along_axis(intersection_1, 'Z', target=pr_cyl, opposite=True)
        # intersection_1.name = "Intersection 1"

        # intersection_2 = new_empty()
        # position_on_curve(intersection_2, line, position=1)
        # copy_rotation(intersection_2, line)
        # project_along_axis(intersection_2, 'Z', target=pr_cyl, opposite=True)
        # intersection_2.name = "Intersection 2"

        return {'FINISHED'}
