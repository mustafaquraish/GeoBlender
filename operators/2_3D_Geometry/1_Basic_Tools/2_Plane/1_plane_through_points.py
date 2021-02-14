import bpy
from GeoBlender.utils.objects import new_plane
from GeoBlender.geometry.planes import align_to_plane_of

class Plane(bpy.types.Operator):
    bl_label = "Plane through 3 points"
    bl_idname = "geometry.3d_plane_points"
    bl_description = "Add a plane going through 3 point. Select the 3 points."
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    plane_size: bpy.props.FloatProperty(
        name="Plane size:",
        description="Length of side of plane",
        soft_min=100,
        soft_max=1000,
        default=100
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3)

    def execute(self, context):
        A, B, C = context.selected_objects[-3:]
        plane = new_plane(size=self.plane_size)
        align_to_plane_of(plane, A, B , C)

        return {'FINISHED'}
