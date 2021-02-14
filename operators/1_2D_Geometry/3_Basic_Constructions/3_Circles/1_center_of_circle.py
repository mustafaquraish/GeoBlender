import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.lines import midpoint, line_ends
from GeoBlender.utils.constraints import copy_transforms


class CenterOfCircle(bpy.types.Operator):
    bl_label = "Center of circle"
    bl_idname = "geometry.center_circle"
    bl_description = ("Returns the center of a circle. Select a circle")
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

        if (len(context.selected_objects) == 1):
            A = context.active_object

            if isinstance(A.data, bpy.types.Curve):
                return 'Circle' in A.data.name

        return False

    def invoke(self, context, event):
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        obj = new_point(use_spheres=self.use_spheres,
                        radius=self.sphere_radius)
        copy_transforms(obj, A, 'LR')

        return {'FINISHED'}
