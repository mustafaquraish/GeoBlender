import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.circles import circle_tangent_lines
from GeoBlender.geometry.circles import circle_tangent_points


class TangentsFromOutside(bpy.types.Operator):
    bl_label = "Tangents from outside point"
    bl_idname = "geometry.tangents_outside"
    bl_description = ("Returns the two tangents from "
                      "a point outside a circle. Select a point and a circle. "
                      "The point should be the active object.")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of tangents",
        min=0,
        soft_max=0.5,
        default=0.2,
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
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        point1 = new_point()
        point2 = new_point()
        circle_tangent_points(point1, point2, B, A)

        line1 = new_line()
        add_abs_bevel(line1, self.bevel_depth)
        line2 = new_line()
        add_abs_bevel(line2, self.bevel_depth)

        circle_tangent_lines(line1, line2, B, A, hide_extra=self.hide_extra)

        return {'FINISHED'}
