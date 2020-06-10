import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.triangles import angle_bisector, angle_divider_foot
from GeoBlender.geometry.lines import segment, ray, line


class AngleBisector(bpy.types.Operator):
    bl_label = "Angle divider"
    bl_idname = "geometry.angle_divider"
    bl_description = ("Adds the angle divider of an angle."
                      " Select three points defining the angle."
                      " The vertex of the angle should be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    use_ray: bpy.props.BoolProperty(
        name="Display ray:",
        description="Display angle bisector as ray otherwise as full line",
        default=True
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of ray",
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

    division_proportion: bpy.props.FloatProperty(
        name="Division proporition:",
        description="Proportion of division of angle by angle divider",
        min=0,
        soft_max=1,
        default=0.5,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        (B, C) = others

        point1 = new_point(hide=True)

        angle_divider_foot(point1, A, B, C,
                           influ=self.division_proportion)

        line1 = new_line()
        add_abs_bevel(line1, self.bevel_depth)

        if self.use_ray:
            ray(line1, A, point1)

        else:
            line(line1, A, point1)

        return {'FINISHED'}
