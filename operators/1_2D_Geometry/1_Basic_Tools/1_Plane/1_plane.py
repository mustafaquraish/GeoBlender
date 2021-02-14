import bpy
from GeoBlender.utils.objects import new_plane


class Plane(bpy.types.Operator):
    bl_label = "Plane"
    bl_idname = "geometry.plane"
    bl_description = "Add a plane"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    plane_size: bpy.props.FloatProperty(
        name="Plane size:",
        description="Length of side of plane",
        soft_min=100,
        soft_max=1000,
        default=300
    )

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        self.plane_size = context.scene.geoblender_settings.plane_size
        return self.execute(context)

    def execute(self, context):
        new_plane(size=self.plane_size)
        return {'FINISHED'}
