import bpy
from GeoBlender.utils.objects import new_point, new_line, add_abs_bevel
from GeoBlender.geometry.triangles import external_bisector


class ExternalBi(bpy.types.Operator):
    bl_label = "External bisector"
    bl_idname = "geometry.angle_bis_ext"
    bl_description = (
        "Add the external angle bisector of a triangle. Select three"
        " points for the"
        " vertices of the triangle. The vertex of the bisector "
        "should be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of angle bisector",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of line",
        min=0,
        soft_max=300,
        default=100,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        (B, C) = others

        med = new_line(length=self.length)
        add_abs_bevel(med, self.bevel_depth)
        external_bisector(med, A, B, C)

        return {'FINISHED'}
