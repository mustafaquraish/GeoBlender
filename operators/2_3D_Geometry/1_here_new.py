import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.inversions import inversion_point


class InversionPoinSft3d(bpy.types.Operator):
    bl_label = "3D construction here"
    bl_idname = "geometry.inversion_point_scd"
    bl_description = ("Write Latex expression")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties.",
        default=True,
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) == 2 and
                context.object is not None):
            A = context.active_object
            others = context.selected_objects[-2:]
            others.remove(A)
            B = others[0]

            if not (isinstance(B.data, bpy.types.Curve)):
                return False

            if not (isinstance(A.data, bpy.types.Mesh)):
                return False

            elif 'Circle' not in B.data.name:
                return False

            else:
                return True

        else:
            return False

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        inv_point = new_point(use_spheres=self.use_spheres,
                              radius=self.sphere_radius)
        inversion_point(inv_point, A, B)

        return {'FINISHED'}
