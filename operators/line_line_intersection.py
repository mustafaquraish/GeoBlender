import bpy
from ..utils.objects import new_empty, new_plane
from ..utils.geometry import make_orthogonal_to
from ..utils.constraints import position_on_curve, copy_transforms
from ..utils.constraints import project_along_axis


class LineLineIntersection(bpy.types.Operator):
    bl_label = "Line-Line Intersection"
    bl_idname = "geometry.empty_intersection"
    bl_description = "Place empty at the intersection of 2 lines"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    gb_panel = 'Planar Intersections'  # GeoBlender Panel for the operator

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for orthocenter",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) and
                isinstance(B.data, bpy.types.Curve)):
            return False
        
        if (not ('Line' in A.data.name and 'Line' in B.data.name)):
            return False

        return True

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        a_start = new_empty(hide=self.hide_extra)
        position_on_curve(a_start, A, 0)

        a_end = new_empty(hide=self.hide_extra)
        position_on_curve(a_end, A, 1)

        pr_plane = new_plane(hide=self.hide_extra)
        make_orthogonal_to(pr_plane, a_start, a_end, B)

        intersection = new_empty()
        copy_transforms(intersection, B, transforms='LR')
        project_along_axis(intersection, 'Z', target=pr_plane, opposite=True)
        intersection.name = "Intersection"

        return {'FINISHED'}
