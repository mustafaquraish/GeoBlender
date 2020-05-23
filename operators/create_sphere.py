import bpy
from ..utils.objects import new_sphere
from ..utils.constraints import copy_location
from ..utils.drivers import add_driver_distance


class CreateSphere(bpy.types.Operator):
    bl_label = "Create Sphere"
    bl_idname = "geometry.create_sphere"
    bl_description = "Create a sphere through a given center and point"
    bl_options = {'REGISTER', 'UNDO'}

    # GeoBlender Panel Type
    gb_panel = '3D Constructions'

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        # B is the point on the sphere, A is the center
        B = context.active_object
        others = context.selected_objects[-2:]
        others.remove(B)
        A = others[0]

        sphere = new_sphere(segments=64)
        copy_location(sphere, A)

        add_driver_distance(sphere, 'scale', 'XYZ', A, B)

        sphere.name = "Sphere"

        return {'FINISHED'}
