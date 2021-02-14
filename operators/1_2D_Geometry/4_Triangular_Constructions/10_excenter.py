import bpy
from GeoBlender.utils.objects import new_point, new_line, add_abs_bevel
from GeoBlender.geometry.triangles import median, excenter


class Incenter(bpy.types.Operator):
    bl_label = "Excenter"
    bl_idname = "geometry.excenter"
    bl_description = ("Add the excenter of a triangle. Select three points. "
                      "The vertex opposite to the excenter should be the "
                      "active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    use_spheres: bpy.props.BoolProperty(
        name="Sphere for excenter:",
        description="Use sphere for excenter. Otherwise use empty",
        default=True
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of sphere drawn for excenter",
        soft_min=0.01,
        soft_max=2,
        default=0.5
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        (B, C) = others

        point = new_point(use_spheres=self.use_spheres,
                          radius=self.sphere_radius)

        excenter(point, A, B, C)

        return {'FINISHED'}
