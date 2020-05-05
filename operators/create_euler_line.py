import bpy
from ..utils.objects import new_empty, new_line, move_origin_center
from ..utils.geometry import put_in_between
from ..utils.geometry import put_at_barycenter, put_at_circumcenter
from ..utils.constraints import damped_track
from ..utils.drivers import add_driver_distance


class CreateEulerLine(bpy.types.Operator):
    bl_label = "Create Euler Line"
    bl_idname = "geometry.create_euler_line"
    bl_description = "Form the euler line of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for euler line",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Depth for circle bevel",
        soft_min=0.0,
        soft_max=0.5,
        default=0.0,
    )

    scale: bpy.props.FloatProperty(
        name="Length:",
        description="Length of Euler Line",
        min=0,
        soft_max=100,
        default=30,
    )

    def execute(self, context):

        if (len(context.selected_objects) != 3):
            self.report({'ERROR'}, 'Need to select 3 objects')
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]

        circumcenter = new_empty(hide=self.hide_extra)
        put_at_circumcenter(circumcenter, A, B, C, hide_extra=self.hide_extra)

        barycenter = new_empty(hide=self.hide_extra)
        put_at_barycenter(barycenter, A, B, C, hide_extra=self.hide_extra)

        line = new_line()
        move_origin_center(line)
        put_in_between(line, circumcenter, barycenter, influence=0.5)
        damped_track(line, axis="Z", target=circumcenter)
        line.scale[2] = self.scale
        # add_driver_distance(
        #     obj=line,
        #     prop='scale',
        #     fields='Z',
        #     A=circumcenter,
        #     B=barycenter,
        #     scale=self.scale
        # )
        line.data.bevel_depth = self.bevel_depth

        return {'FINISHED'}