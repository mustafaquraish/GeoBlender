import bpy
from GeoBlender.utils.objects import new_point
from GeoBlender.geometry.planes import constraint_to_plane
from GeoBlender.utils.drivers import add_driver


class PointOnPlane(bpy.types.Operator):
    bl_label = "Point on plane"
    bl_idname = "geometry.point_on_plane"
    bl_description = ("Add a point constrained on a plane. "
                      "Select a plane")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions > Basic Tools > Points'

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

    @classmethod
    def poll(cls, context):

        if (len(context.selected_objects) != 1):
            return False

        A = context.active_object

        if not (isinstance(A.data, bpy.types.Mesh)):
            return False

        if 'Plane' not in A.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        plane = context.active_object

        created_point = new_point(use_spheres=self.use_spheres,
                                  radius=self.sphere_radius
                                  )
        created_point.name = 'Point'

        constraint_to_plane(created_point, plane)

        add_driver(obj=created_point,
                   prop='scale',
                   fields='XYZ',
                   vars_def={'x1': ('transform', plane, 'scale', 'X'),
                             },
                   expr="1/ x1")

        return {'FINISHED'}
