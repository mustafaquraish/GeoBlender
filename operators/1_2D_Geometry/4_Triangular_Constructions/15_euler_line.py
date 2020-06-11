import bpy
from GeoBlender.utils.objects import new_point, new_line, add_abs_bevel
from GeoBlender.geometry.triangles import euler_line


class EulerLine(bpy.types.Operator):
    bl_label = "Euler line"
    bl_idname = "geometry.euler_line"
    bl_description = ("Add the Euler line of a triangle."
                      " Select three points")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of tangent",
        min=0,
        soft_max=300,
        default=100,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length

        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]

        line1 = new_line(length=self.length)
        add_abs_bevel(line1, self.bevel_depth)

        euler_line(line1, A, B, C)

        return {'FINISHED'}
