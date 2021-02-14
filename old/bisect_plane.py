import bpy
from ..utils.objects import new_plane, uniform_scale
from ..geometry.planes import bisecting_plane_of_points


class BisectPlane(bpy.types.Operator):
    bl_label = "Bisecting Plane"
    bl_idname = "geometry.bisect_plane"
    bl_description = "Make a plane orthogonal to the line connecting 2 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '3D Constructions'

    size: bpy.props.FloatProperty(
        name="Size:",
        description="Size of the Plane",
        min=0.0,
        soft_max=100,
        default=10,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2)

    def execute(self, context):

        (A, B) = context.selected_objects[-2:]

        plane = new_plane(size=self.size)
        bisecting_plane_of_points(plane, A, B)
        plane.name = "Perp. Bisector Plane"
        uniform_scale(plane, self.size)

        return {'FINISHED'}
