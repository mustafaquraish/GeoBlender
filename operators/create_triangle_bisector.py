import bpy
from ..utils.objects import new_line, new_empty, new_plane
from ..utils.geometry import stretch_between_points
from ..utils.geometry import make_orthogonal_to, track_to_angle_between
from ..utils.constraints import copy_location, project_along_axis


class CreateTriangleBisector(bpy.types.Operator):
    bl_label = "Create Triangle Bisector"
    bl_idname = "geometry.create_triangle_bisector"
    bl_description = "Form the bisector of the triangle from active vertex"
    bl_options = {'REGISTER', 'UNDO'}

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for triangle bisector",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        if (len(context.selected_objects) != 3):
            self.report({'ERROR'}, 'Need to select 3 objects')
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]
        active = context.active_object

        if active is None:
            self.report({'ERROR'}, 'No active object selected')
            return {'CANCELLED'}

        others = [A, B, C]
        others.remove(active)

        pr_plane = new_plane(hide=self.hide_extra)
        pr_plane.name = "projection plane"
        make_orthogonal_to(pr_plane, others[0], others[1], active, axis='Z')

        bisector_point = new_empty(hide=self.hide_extra)
        bisector_point.name = "bisector point"
        copy_location(bisector_point, active)
        track_to_angle_between(bisector_point, others[0], others[1])
        project_along_axis(
            bisector_point,
            axis='X',
            target=pr_plane,
            opposite=True
        )

        line = new_line()
        stretch_between_points(line, active, bisector_point, axis='Z')
        line.data.bevel_depth = self.bevel_depth
        line.name = "Bisector"

        return {'FINISHED'}
