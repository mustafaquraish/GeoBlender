import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.lines import line_ends, segment
from GeoBlender.geometry.lines import parallel_line


class ParallelLine(bpy.types.Operator):
    bl_label = "Parallel line"
    bl_idname = "geometry.parallel_line"
    bl_description = ("Returns the line through a given point and"
                      " parallel to a line. Select either three points"
                      " or a point"
                      " and a line. The point the parallel line passes"
                      " through needs to be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

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

    @classmethod
    def poll(cls, context):

        if (len(context.selected_objects) == 3):
            return True

        if (len(context.selected_objects) == 2):

            A = context.active_object
            others = context.selected_objects[-2:]
            others.remove(A)
            B = others[0]

            if not (isinstance(B.data, bpy.types.Curve)):
                return False

            elif 'Line' not in B.data.name:
                return False

            else:
                return True

        else:
            return False

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length
        return self.execute(context)

    def execute(self, context):

        if (len(context.selected_objects) == 3):
            A = context.active_object
            others = context.selected_objects[-3:]
            others.remove(A)
            (B, C) = others
            line = new_line(hide=self.hide_extra)
            segment(line, B, C)

            obj = new_line(length=self.length)
            add_abs_bevel(obj, self.bevel_depth)

            parallel_line(obj, A, line, hide_extra=self.hide_extra)

        if (len(context.selected_objects) == 2):
            A = context.active_object
            others = context.selected_objects[-2:]
            others.remove(A)
            line = others[0]
            obj = new_line(length=self.length)
            add_abs_bevel(obj, self.bevel_depth)

            parallel_line(obj, A, line, hide_extra=self.hide_extra)

        return {'FINISHED'}
