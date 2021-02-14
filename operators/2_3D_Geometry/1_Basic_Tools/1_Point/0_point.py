import bpy
from GeoBlender.utils.objects import new_point
from GeoBlender.geometry.planes import constraint_to_plane
from GeoBlender.utils.drivers import add_driver


class PointOnPlane(bpy.types.Operator):
    bl_label = "Add a point"
    bl_idname = "geometry.3d_add_point"
    bl_description = ("Add an unconstrained point")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties.",
        default=True,
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
    )

    def execute(self, context):
        created_point = new_point(
            use_spheres=self.use_spheres,
            radius=self.sphere_radius
        )
        created_point.name = 'Point'
        return {'FINISHED'}
