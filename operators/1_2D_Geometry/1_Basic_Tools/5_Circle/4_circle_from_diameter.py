import bpy
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.geometry.circles import circle_from_diameter
from GeoBlender.geometry.lines import line_ends


class CircleDiameter(bpy.types.Operator):
    bl_label = "Circle with diameter"
    bl_idname = "geometry.circle_diameter"
    bl_description = ("Add a circle with given diameter. Select either the "
                      "antidiametrical points or the diameter")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) == 1):
            if context.object is None:
                return False
            else:
                line = context.active_object
                if (isinstance(line.data, bpy.types.Curve)):
                    if ('Line' in line.data.name):
                        return True
                    else:
                        return False
                else:
                    return False
        elif (len(context.selected_objects) == 2):
            return True
        else:
            return False

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra

        return self.execute(context)

    def execute(self, context):

        line = context.active_object

        if (isinstance(line.data, bpy.types.Curve)):
            A = new_point(hide=self.hide_extra)
            B = new_point(hide=self.hide_extra)
            line_ends(A, B, line)
            circle = new_circle()
            circle_from_diameter(circle, A, B)
            add_abs_bevel(circle, self.bevel_depth)

        else:
            (A, B) = context.selected_objects[-2:]
            circle = new_circle()
            circle_from_diameter(circle, A, B)
            add_abs_bevel(circle, self.bevel_depth)

        return {'FINISHED'}
