import bpy
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.geometry.triangles import excircle

class Circumcircle(bpy.types.Operator):
    bl_label = "Excircle"
    bl_idname = "geometry.excircle"
    bl_description = ("Add the excircle of a triangle."
                     " Select three points."
                     " The vertex opposite to the excircle should be the"
                     " active object")
                      
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.2,
    )
      
    
    hide_center: bpy.props.BoolProperty(
        name="Hide center:",
        description="Hide the center of the circle",
        default=False
        )
    

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties",
        default=True
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5
    )

    
    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        (B, C) = others

        center = new_point(use_spheres=self.use_spheres,
                           radius=self.sphere_radius,
                           hide=self.hide_center)

        

        circle = new_circle()
        excircle(circle, center, A, B, C)
        add_abs_bevel(circle, self.bevel_depth)

        return {'FINISHED'}
