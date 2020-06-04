import bpy
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.geometry.triangles import circumcircle


class Circumcircle(bpy.types.Operator):
    bl_label = "Circumcircle"
    bl_idname = "geometry.circumc"
    bl_description = ("Add the circumcircle of a triangle."
                      " Select three points")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    hide_center: bpy.props.BoolProperty(
        name="Hide center:",
        description="Hide the center of the circle",
        default=False
    )

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
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]

        center = new_point(use_spheres=self.use_spheres,
                           radius=self.sphere_radius,
                           hide=self.hide_center)

        circle = new_circle()
        circumcircle(circle, center, A, B, C)
        add_abs_bevel(circle, self.bevel_depth)

        return {'FINISHED'}
