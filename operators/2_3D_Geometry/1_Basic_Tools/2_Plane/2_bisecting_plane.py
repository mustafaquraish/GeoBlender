import bpy
from GeoBlender.utils.objects import new_plane
from GeoBlender.geometry.planes import bisecting_plane_of_points
from GeoBlender.geometry.planes import bisecting_plane_of_line


class Plane(bpy.types.Operator):
    bl_label = "Perp. Bisecting plane"
    bl_idname = "geometry.3d_bisecting_plane"
    bl_description = "Make perp. bisecting plane of 2 points / a segment. " +\
                     "Select the 2 points or a line segment."
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    plane_size: bpy.props.FloatProperty(
        name="Plane size:",
        description="Length of side of plane",
        soft_min=100,
        soft_max=1000,
        default=300
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) == 1):
            A = context.object
            if A != context.selected_objects[0]:
                return False
            if isinstance(A.data, bpy.types.Curve):
                return ('Line' in A.data.name)
            return False

        return len(context.selected_objects) == 2

    def execute(self, context):

        plane = new_plane(size=self.plane_size)
        plane.name = "Perp. Bisecting Plane"

        if len(context.selected_objects) == 1:
            bisecting_plane_of_line(plane, context.object)
        else:
            A, B = context.selected_objects[-2:]
            bisecting_plane_of_points(plane, A, B)

        return {'FINISHED'}
