import bpy
from ..utils.objects import new_arc
from ..utils.drivers import add_driver_distance
from ..utils.geometry import put_in_between
from ..utils.constraints import damped_track


class CreateSemicircle(bpy.types.Operator):
    bl_label = "Create Semicircle"
    bl_idname = "geometry.create_semicircle"
    bl_description = "Create Semicircle through diametrically opposed points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions'

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    change_side: bpy.props.BoolProperty(
        name="Change Side:",
        description="Change which side the semicircle is drawn",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        semi = new_arc()
        put_in_between(semi, A, B, influence=0.5)

        # Change the side of the semicircle by tracking in neg. dir.
        if (self.change_side):
            damped_track(semi, axis='-X', target=B)
        else:
            damped_track(semi, axis='X', target=B)

        add_driver_distance(
            obj=semi,
            prop='scale',
            fields='XY',
            A=A,
            B=B,
            scale=0.5
        )
        semi.name = "Semicircle"
        semi.data.bevel_depth = self.bevel_depth

        return {'FINISHED'}
