import bpy
from ..utils.objects import new_line, new_empty, new_plane, add_abs_bevel
from ..utils.geometry import stretch_between_points, make_orthogonal_to
from ..utils.constraints import copy_location, project_nearest


class CreateTriangleAltitude(bpy.types.Operator):
    bl_label = "Create Triangle Altitude"
    bl_idname = "geometry.create_triangle_altitude"
    bl_description = "Form the altitude of the triangle from active vertex"
    bl_options = {'REGISTER', 'UNDO'}

    # GeoBlender Panel Type
    gb_panel = 'Triangle Constructions'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for triangle altitude",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]
        active = context.active_object

        others = [A, B, C]
        others.remove(active)

        pr_plane = new_plane(hide=self.hide_extra)
        pr_plane.name = "projection plane"
        make_orthogonal_to(pr_plane, others[0], others[1], active, axis='Z')

        altitude_point = new_empty(hide=self.hide_extra)
        altitude_point.name = "altitude projection"
        copy_location(altitude_point, active)
        project_nearest(altitude_point, target=pr_plane)

        line = new_line()
        stretch_between_points(line, active, altitude_point, axis='Z')
        add_abs_bevel(line, self.bevel_depth)
        line.name = "Altitude"

        return {'FINISHED'}
