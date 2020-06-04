import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.lines import orthogonal_proj_to_points
from GeoBlender.geometry.lines import orthogonal_proj_to_line


class OrthProj(bpy.types.Operator):
    bl_label = "Orthogonal projection"
    bl_idname = "geometry.ortho_proje"
    bl_description = ("Returns the orthogonal projection of a point on"
                      " a line. Select either three points or a point"
                      " and a line. The point that is projected should"
                      " be the active object")
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
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        if (len(context.selected_objects) == 3):
            A = context.active_object
            others = context.selected_objects[-3:]
            others.remove(A)
            (B, C) = others

            obj = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius)

            orthogonal_proj_to_points(obj, A, B, C)

        if (len(context.selected_objects) == 2):
            A = context.active_object
            others = context.selected_objects[-2:]
            others.remove(A)
            B = others[0]
            obj = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius)

            orthogonal_proj_to_line(obj, A, B)

        return {'FINISHED'}
