import bpy
from ..utils.objects import new_empty, new_cylinder
from ..utils.constraints import position_on_curve, copy_transforms
from ..utils.constraints import project_along_axis, copy_rotation


class LineCircleIntersection(bpy.types.Operator):
    bl_label = "Line-Circle Intersection"
    bl_idname = "geometry.line_circle_intersection"
    bl_description = "Place empty at the intersection of 2 a line " +\
                     "and circle on the same plane"
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

        if 'BezierCircle' in A.data.name and 'Line' in B.data.name:
            circle, line = A, B
        elif 'Line' in A.data.name and 'BezierCircle' in B.data.name:
            circle, line = B, A
        else:
            self.report({'ERROR'}, 'Need to select a line and a circle')
            return {'CANCELLED'}

        pr_cyl = new_cylinder(vert=100, hide=self.hide_extra)
        copy_transforms(pr_cyl, circle)

        intersection_1 = new_empty()
        position_on_curve(intersection_1, line, position=0)
        copy_rotation(intersection_1, line)
        project_along_axis(intersection_1, 'Z', target=pr_cyl, opposite=True)
        intersection_1.name = "Intersection 1"

        intersection_2 = new_empty()
        position_on_curve(intersection_2, line, position=1)
        copy_rotation(intersection_2, line)
        project_along_axis(intersection_2, 'Z', target=pr_cyl, opposite=True)
        intersection_2.name = "Intersection 2"

        return {'FINISHED'}
