import bpy
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.geometry.circles import circle_from_center_point


class CircleCPoint(bpy.types.Operator):
    bl_label = "Circle with center and point"
    bl_idname = "geometry.circle_center_point"
    bl_description = (
        "Add a circle with given center and through a given point. "
        "Select two points, the center should be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions > Basic Tools > Circles'

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    hide_center: bpy.props.BoolProperty(
        name="Hide center:",
        description="Hide the center of the circle.",
        default=False,
        options={'HIDDEN'},
    )

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties.",
        default=True,
        options={'HIDDEN'},
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        circle = new_circle()
        circle_from_center_point(circle, A, B)
        add_abs_bevel(circle, self.bevel_depth)

        return {'FINISHED'}
