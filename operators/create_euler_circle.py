import bpy
from ..utils.objects import new_circle, new_empty
from ..utils.geometry import put_at_circumcenter, put_in_between
from ..utils.constraints import copy_transforms
from ..utils.drivers import add_driver_distance


class CreateEulerCircle(bpy.types.Operator):
    bl_label = "Create Euler Circle"
    bl_idname = "geometry.create_euler_circle"
    bl_description = "Form the euler circle of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for euler circle",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Depth for circle bevel",
        soft_min=0.0,
        soft_max=0.5,
        default=0.0,
    )

    def execute(self, context):

        if (len(context.selected_objects) != 3):
            self.report({'ERROR'}, 'Need to select 3 objects')
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]

        mid_ab = new_empty(hide=self.hide_extra)
        put_in_between(mid_ab, A, B, influence=0.5)

        mid_bc = new_empty(hide=self.hide_extra)
        put_in_between(mid_bc, B, C, influence=0.5)

        mid_ca = new_empty(hide=self.hide_extra)
        put_in_between(mid_ca, C, A, influence=0.5)

        euler_center = new_empty(hide=self.hide_extra)
        euler_center.name = "Euler Circle center"
        put_at_circumcenter(euler_center, mid_ab, mid_bc, mid_ca,
                            hide_extra=self.hide_extra)

        circle = new_circle()
        copy_transforms(circle, target=euler_center, transforms="LR")
        add_driver_distance(circle, 'scale', 'XY', euler_center, mid_ab)
        circle.data.bevel_depth = self.bevel_depth
        circle.name = "Euler Circle"

        return {'FINISHED'}