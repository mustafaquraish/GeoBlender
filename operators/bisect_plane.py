import bpy
from ..utils.objects import new_plane
from ..geometry.planes import make_bisecting_plane


class BisectPlane(bpy.types.Operator):
    bl_label = "Bisecting Plane"
    bl_idname = "geometry.bisect_plane"
    bl_description = "Make a plane orthogonal to the line connecting 2 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '3D Constructions'

    influence: bpy.props.FloatProperty(
        name="Position:",
        description="Influence",
        max=1.0,
        min=0.0,
        default=0.5,
    )

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
        make_bisecting_plane(plane, A, B)
        plane.name = "Perp. Bisector Plane"

        return {'FINISHED'}
