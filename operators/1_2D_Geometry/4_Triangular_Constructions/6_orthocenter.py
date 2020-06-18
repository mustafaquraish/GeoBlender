import bpy
from GeoBlender.utils.objects import new_point, new_line, add_abs_bevel
from GeoBlender.geometry.triangles import median, orthocenter


class Ortho(bpy.types.Operator):
    bl_label = "Orthocenter"
    bl_idname = "geometry.ortho"
    bl_description = ("Add the orthocenter of a triangle. Select three points")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    use_spheres: bpy.props.BoolProperty(
        name="Sphere for mid point:",
        description="Use sphere for mid point. Otherwise use empty",
        default=True
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of sphere drawn for mid point",
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

        point = new_point(use_spheres=self.use_spheres,
                          radius=self.sphere_radius)

        orthocenter(point, A, B, C)

        return {'FINISHED'}
