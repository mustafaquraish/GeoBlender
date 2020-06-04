import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.lines import midpoint, line_ends


class Midpoint(bpy.types.Operator):
    bl_label = "Mid point"
    bl_idname = "geometry.mid_point"
    bl_description = ("Returns the mid point of a segment. Select either two"
                      " points or a line segment")
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

        if (len(context.selected_objects) == 2):
            return True

        if (len(context.selected_objects) == 1):
            A = context.active_object

            if not (isinstance(A.data, bpy.types.Curve)):
                return False

            elif 'Line' not in A.data.name:
                return False

            else:
                return True

        else:
            return False

    def invoke(self, context, event):
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        if (len(context.selected_objects) == 2):
            (A, B) = context.selected_objects[-2:]
            obj = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius)

            midpoint(obj, A, B)

        if (len(context.selected_objects) == 1):
            A = context.active_object
            X = new_point(hide=self.hide_extra)
            Y = new_point(hide=self.hide_extra)
            line_ends(X, Y, A)
            obj = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius)

            midpoint(obj, X, Y)

        return {'FINISHED'}
