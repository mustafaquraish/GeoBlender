import bpy
from GeoBlender.utils.objects import new_point, new_sphere, add_abs_bevel
from GeoBlender.geometry.spheres import sphere_from_center_radius


class CirceCeRa(bpy.types.Operator):
    bl_label = "Sphere with center and radius"
    bl_idname = "geometry.3d_sphere_center_radius"
    bl_description = ("Add a sphere with given center and radius. "
                      "Select a point for the center")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    segments: bpy.props.IntProperty(
        name="Resolution:",
        description="Resolution for the Sphere",
        min=3,
        soft_max=150,
        default=64,
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of sphere",
        soft_min=0.01,
        soft_max=200,
        default=5,
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) == 1
                and context.object is not None):

            A = context.active_object
            return (not isinstance(A.data, bpy.types.Curve))

        return False

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):

        A = context.active_object

        sphere = new_sphere(segments=self.segments)
        sphere_from_center_radius(sphere, A, self.sphere_radius)

        return {'FINISHED'}
