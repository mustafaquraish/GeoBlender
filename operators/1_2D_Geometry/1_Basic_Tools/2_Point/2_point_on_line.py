import bpy
from GeoBlender.utils.objects import new_point
from GeoBlender.utils.constraints import position_on_curve
from GeoBlender.utils.constraints import copy_rotation
from GeoBlender.utils.drivers import add_driver


class PointOnLine(bpy.types.Operator):
    bl_label = "Point on line"
    bl_idname = "geometry.point_on_line"
    bl_description = "Add a point constrained on a line. Select a line"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties.",
        default=True
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5
    )

    position_c: bpy.props.FloatProperty(
        name="Position on line:",
        description="Set the position of the point on the line",
        soft_min=0,
        soft_max=1,
        default=0
    )

    @classmethod
    def poll(cls, context):

        if (len(context.selected_objects) != 1):
            return False

        B = context.active_object

        if not (isinstance(B.data, bpy.types.Curve)):
            return False

        if 'Circle' in B.data.name:
            return False

        if 'Arc' in B.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        line = context.active_object

        A = new_point(use_spheres=self.use_spheres, radius=self.sphere_radius)
        A.name = 'Point'

        add_driver(
            obj=A,
            prop='location',
            fields='XYZ',
            expr="0"
        )
        position_on_curve(A, line, position=self.position_c)
        copy_rotation(A, line)

        return {'FINISHED'}
