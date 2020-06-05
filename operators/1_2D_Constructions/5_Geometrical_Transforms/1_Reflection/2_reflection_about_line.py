import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.lines import reflect_across_line
from GeoBlender.geometry.lines import reflect_across_line_of_points


class MidpointRef(bpy.types.Operator):
    bl_label = "Reflection about a line"
    bl_idname = "geometry.reflection_line"
    bl_description = ("Returns the reflection of a point relative to a line."
                      " Select a point and a line or three points. The point"
                      " to be reflected should be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties.",
        default=True,
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
    )

    @classmethod
    def poll(cls, context):

        if (len(context.selected_objects) == 2 and
                context.object is not None):
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

        if (len(context.selected_objects) == 3 and
                context.object is not None):
            return True
        else:
            return False

    def invoke(self, context, event):
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        if (len(context.selected_objects) == 2 and
                context.object is not None):
            A = context.active_object
            others = context.selected_objects[-2:]
            others.remove(A)
            B = others[0]

            reflect_point = new_point(use_spheres=self.use_spheres,
                                      radius=self.sphere_radius)
            reflect_across_line(reflect_point, A, B)

        if (len(context.selected_objects) == 3 and
                context.object is not None):
            A = context.active_object
            others = context.selected_objects[-3:]
            others.remove(A)
            (B, C) = others

            reflect_point = new_point(use_spheres=self.use_spheres,
                                      radius=self.sphere_radius)
            reflect_across_line_of_points(reflect_point, A, B, C)

        return {'FINISHED'}
