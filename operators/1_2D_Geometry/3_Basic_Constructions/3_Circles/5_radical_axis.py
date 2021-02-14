import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.circles import radical_axis, radical_intercept
from GeoBlender.utils.constraints import copy_transforms
from GeoBlender.utils.objects import move_origin_center


class RadicalAxis(bpy.types.Operator):
    bl_label = "Radical axis"
    bl_idname = "geometry.radical_axis"
    bl_description = ("Returns the radical axis two circles. "
                      "Select two circles")
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

        if not (len(context.selected_objects) == 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve)):
            return False

        if not (isinstance(B.data, bpy.types.Curve)):
            return False

        if 'Circle' not in A.data.name:
            return False

        if 'Circle' not in B.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.length = context.scene.geoblender_settings.length
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]
        point_r = new_point(hide=True)
        radical_intercept(point_r, A, B)
        line1 = new_line(length=self.length)
        add_abs_bevel(line1, self.bevel_depth)

        radical_axis(line1, A, B)

        return {'FINISHED'}
