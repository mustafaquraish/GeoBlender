import bpy
from ..utils.objects import new_line, new_empty
from ..utils.geometry import stretch_between_points, put_in_between


class CreateTriangleMedian(bpy.types.Operator):
    bl_label = "Create Triangle Median"
    bl_idname = "geometry.create_triangle_median"
    bl_description = "Form the median of the triangle from active vertex"
    bl_options = {'REGISTER', 'UNDO'}

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for triangle median",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    def execute(self, context):

        if (len(context.selected_objects) != 3):
            self.report({'ERROR'}, 'Need to select 3 objects')
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]
        active = context.active_object
        others = [A, B, C]
        others.remove(active)

        mid_op = new_empty(hide=self.hide_extra)
        mid_op.name = "opposite side midpoint"
        put_in_between(mid_op, others[0], others[1], influence=0.5)

        line = new_line()
        stretch_between_points(line, active, mid_op, axis='Z')
        line.data.bevel_depth = self.bevel_depth
        line.name = "Median"

        return {'FINISHED'}
