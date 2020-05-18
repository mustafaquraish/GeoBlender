import bpy
from ..utils.objects import new_empty, new_plane, new_sphere
from ..utils.geometry import put_at_circumcenter, put_in_between
from ..utils.constraints import copy_transforms, project_along_axis
from ..utils.constraints import damped_track
from ..utils.drivers import add_driver_distance


class CreateCircumsphere(bpy.types.Operator):
    bl_label = "Create Circumsphere"
    bl_idname = "geometry.create_circumsphere"
    bl_description = "Form the circumsphere of the 4 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '3D Constructions'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for circumsphere",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 4)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B, C, D) = context.selected_objects[-4:]

        pr_plane = new_plane(hide=self.hide_extra)
        pr_plane.name = 'projection plane'
        put_in_between(pr_plane, A, D)
        damped_track(pr_plane, axis='Z', target=A)

        center = new_empty(hide=self.hide_extra)
        center.name = 'sphere center'
        put_at_circumcenter(center, A, B, C, hide_extra=self.hide_extra)
        project_along_axis(center, axis='Z', target=pr_plane, opposite=True)

        circumsphere = new_sphere(segments=64, rings=32)
        copy_transforms(circumsphere, target=center, transforms='LR')
        add_driver_distance(
            obj=circumsphere,
            prop='scale',
            fields='XYZ',
            A=A,
            B=center
        )
        circumsphere.name = 'Circumsphere'

        return {'FINISHED'}
