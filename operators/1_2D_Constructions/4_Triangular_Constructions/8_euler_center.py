import bpy
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.geometry.triangles import euler_center

class Circumcenter(bpy.types.Operator):
    bl_label = "Euler center"
    bl_idname = "geometry.circumcece"
    bl_description = ("Add the Euler center of a triangle."
                     " Select three points")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type

       

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties",
        default=True
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5
    )

    
    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3)

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]

        center = new_point(use_spheres=self.use_spheres,
                           radius=self.sphere_radius)                         

        
        euler_center(center, A, B, C)

        return {'FINISHED'}
