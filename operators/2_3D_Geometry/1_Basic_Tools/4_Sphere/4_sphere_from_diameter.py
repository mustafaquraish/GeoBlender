import bpy
from GeoBlender.utils.objects import new_point, new_sphere, add_abs_bevel
from GeoBlender.geometry.spheres import sphere_from_diameter
from GeoBlender.geometry.lines import line_ends


class SphereDiameter(bpy.types.Operator):
    bl_label = "Sphere with diameter"
    bl_idname = "geometry.3d_sphere_diameter"
    bl_description = ("Add a sphere with given diameter. Select either the "
                      "antidiametrical points or the diameter")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for circumsphere",
        default=True,
    )

    segments: bpy.props.IntProperty(
        name="Resolution:",
        description="Resolution for the Sphere",
        min=3,
        soft_max=150,
        default=64,
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) == 1):
            if context.object is None:
                return False

            line = context.active_object
            if (isinstance(line.data, bpy.types.Curve)):
                return ('Line' in line.data.name)

            return False

        else:
            return (len(context.selected_objects) == 2)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        line = context.active_object
        sphere = new_sphere(segments=self.segments)

        if isinstance(line.data, bpy.types.Curve):
            A = new_point(hide=self.hide_extra)
            B = new_point(hide=self.hide_extra)
            line_ends(A, B, line)
            sphere_from_diameter(sphere, A, B)

        else:
            (A, B) = context.selected_objects[-2:]
            sphere_from_diameter(sphere, A, B)

        return {'FINISHED'}
