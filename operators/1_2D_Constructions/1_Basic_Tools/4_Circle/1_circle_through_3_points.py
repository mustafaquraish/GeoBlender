import bpy
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.geometry.triangles import circumcircle

class CircleThrough3Points(bpy.types.Operator):
    bl_label = "Circle through 3 points"
    bl_idname = "geometry.circle_through_3_points"
    bl_description = "Add a circle through 3 points"
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
        return (len(context.selected_objects) == 3)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]

        center = new_point(use_spheres=self.use_spheres,
                           radius=self.sphere_radius,
                           hide=self.hide_center)

        # Local properties are not available for when creating points! Here for the center
        # in previously for simply adding points (on plane, lines, etc.)


        circle = new_circle()
        circumcircle(circle, center, A, B, C)
        add_abs_bevel(circle, self.bevel_depth)

        return {'FINISHED'}
