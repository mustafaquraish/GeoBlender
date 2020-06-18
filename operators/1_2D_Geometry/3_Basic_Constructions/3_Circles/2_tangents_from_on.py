import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.circles import circle_tangent_line
from GeoBlender.geometry.circles import circle_tangent_points


class TangentsFromOn(bpy.types.Operator):
    bl_label = "Tangent at a point"
    bl_idname = "geometry.tangents_on"
    bl_description = ("Returns the tangent at a point on the circle. "
                      "Select a point and a circle. "
                      "The point should be the active object.")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of tangent",
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
        if (len(context.selected_objects) != 2):
            return False

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        if not (isinstance(A.data, bpy.types.Mesh) and
                isinstance(B.data, bpy.types.Curve)):
            return False

        return 'Circle' in B.data.name

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        self.length = context.scene.geoblender_settings.length
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth

        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        line1 = new_line(length=self.length)
        add_abs_bevel(line1, self.bevel_depth)

        circle_tangent_line(line1, B, A)

        return {'FINISHED'}
