import bpy
from ..utils.objects import new_point


class PointOnPlane(bpy.types.Operator):
    bl_label = "Point on Plane (active)"
    bl_idname = "geometry.point_on_plane"
    bl_description = "Add a point constrained on a plane"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions > Basic Tools > Points'

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties.",
        default=True,
        options={'HIDDEN'},
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.1,
        options={'HIDDEN'},
    )

    sphere_subdivisions: bpy.props.IntProperty(
        name="Segments:",
        description="Segments to use for the spheres for points",
        min=1,
        max=100,
        default=32,
        options={'HIDDEN'},
    )


    @classmethod
    def poll(cls, context):
        
        A = context.active_object

        if not (isinstance(A.data, bpy.types.Mesh)):
            return False

        if 'Plane' not in A.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.sphere_subdivisions = context.scene.geoblender_settings.sphere_subdivisions
        return self.execute(context)

    def execute(self, context):
        plane = context.active_object

        created_point = new_point(use_spheres=self.use_spheres,
                                  radius=self.sphere_radius, 
                                  segments=self.sphere_subdivisions)
        created_point.name = ''Point''

        constraint_to_plane(created_point, plane)

        return {'FINISHED'}