import bpy
from GeoBlender.utils.objects import new_point, new_line, add_abs_bevel
from GeoBlender.geometry.triangles import median, incenter


class Incenter(bpy.types.Operator):
    bl_label = "Incenter"
    bl_idname = "geometry.incenter"
    bl_description = ("Add the incenter of a triangle. Select three points")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    use_spheres: bpy.props.BoolProperty(
        name="Sphere for incenter:",
        description="Use sphere for incenter. Otherwise use empty",
        default=True
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of sphere drawn for incenter",
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

        incenter(point, A, B, C)

        return {'FINISHED'}
