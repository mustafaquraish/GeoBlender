import bpy
from GeoBlender.utils.objects import new_point, new_line, add_abs_bevel
from GeoBlender.geometry.triangles import altitude


class Alti(bpy.types.Operator):
    bl_label = "Altitude"
    bl_idname = "geometry.altitu"
    bl_description = ("Add an altitude of a triangle. Select three points for "
                      "the vertices of the triangle. The vertex of the "
                      "altitude should be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    hide_foot: bpy.props.BoolProperty(
        name="Hide foot:",
        description="Hide the foot of the altitude",
        default=False
    )

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
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        (B, C) = others

        footp = new_point(use_spheres=self.use_spheres,
                          radius=self.sphere_radius,
                          hide=self.hide_foot)

        alt = new_line()
        add_abs_bevel(alt, self.bevel_depth)
        altitude(alt, footp, A, B, C)

        return {'FINISHED'}
