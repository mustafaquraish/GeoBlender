import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_circle
from GeoBlender.geometry.inversions import inversion_line_not_on


class InversionLineOff(bpy.types.Operator):
    bl_label = "Inversion of line (off)"
    bl_idname = "geometry.inversion_line_off"
    bl_description = ("Adds the inversion of a line in the case where the"
                      " line does not go through the origin of inversion."
                      " Select the line (active) and a circle."
                      " The center of the circle is the origin and the "
                      "square of its radius is the power of inversion")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
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
        if (len(context.selected_objects) == 2 and
                context.object is not None):
            A = context.active_object
            others = context.selected_objects[-2:]
            others.remove(A)
            B = others[0]

            if not (isinstance(B.data, bpy.types.Curve) and
                    (isinstance(A.data, bpy.types.Curve))):
                return False

            if 'Circle' not in B.data.name:
                return False

            if 'Line' not in A.data.name:
                return False

            else:
                return True

        else:
            return False

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        inv_line = new_circle()
        add_abs_bevel(inv_line, self.bevel_depth)
        inversion_line_not_on(inv_line, A, B)

        return {'FINISHED'}
