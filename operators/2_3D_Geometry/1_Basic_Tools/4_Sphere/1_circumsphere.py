import bpy
from GeoBlender.utils.objects import new_sphere, new_point
from GeoBlender.geometry.spheres import circumsphere, put_at_circumcenter


class CreateCircumsphere(bpy.types.Operator):
    bl_label = "Create Circumsphere"
    bl_idname = "geometry.3d_circumsphere"
    bl_description = "Form the circumsphere of the 4 points. Select 4 points."
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for circumsphere",
        default=True,
    )

    segments: bpy.props.IntProperty(
        name="Resolution:",
        description="Resolution for the Sphere",
        min=3,
        soft_max=150,
        default=64,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 4)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B, C, D) = context.selected_objects[-4:]

        sphere = new_sphere(segments=self.segments)
        circumsphere(sphere, A, B, C, D, self.hide_extra)
        sphere.name = 'Circumsphere'

        return {'FINISHED'}
