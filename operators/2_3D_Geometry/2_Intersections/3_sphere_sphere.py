import bpy
from GeoBlender.utils.objects import new_circle, add_abs_bevel, new_point
from GeoBlender.geometry.intersections import sphere_sphere_intersection


class SphereSphereInter(bpy.types.Operator):
    bl_label = "Sphere - Sphere"
    bl_idname = "geometry.sphere_sphere"
    bl_description = ("Returns intersections of 2 spheres. Select 2 spheres")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of segment",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    @classmethod
    def poll(cls, context):

        if not (len(context.selected_objects) == 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if 'Sphere' not in A.data.name:
            return False

        if 'Sphere' not in B.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]
        
        circle = new_circle()
        sphere_sphere_intersection(circle, A, B)
        add_abs_bevel(circle, self.bevel_depth)


        return {'FINISHED'}
