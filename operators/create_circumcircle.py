import bpy
from ..utils.objects import new_circle, new_empty
from ..utils.geometry import put_at_circumcenter
from ..utils.constraints import copy_transforms
from ..utils.drivers import add_driver_distance


class CreateCircumcircle(bpy.types.Operator):
    bl_label = "Create Circumcircle"
    bl_idname = "geometry.create_circumcircle"
    bl_description = "Form the circumcircle of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for circumcircle",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Depth for circle bevel",
        soft_min=0.0,
        soft_max=0.5,
        default=0.0,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]

        circumcenter = new_empty(hide=self.hide_extra)
        circumcenter.name = "circumcenter"
        put_at_circumcenter(circumcenter, A, B, C, hide_extra=self.hide_extra)

        circle = new_circle()
        copy_transforms(circle, target=circumcenter, transforms="LR")
        add_driver_distance(circle, 'scale', 'XY', circumcenter, A)
        circle.data.bevel_depth = self.bevel_depth
        circle.name = "Cirumcircle"

        return {'FINISHED'}
