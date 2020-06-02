import bpy
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.geometry.circles import circle_from_center_radius

class CirceCeRa(bpy.types.Operator):
    bl_label = "Circle with center and radius"
    bl_idname = "geometry.circle_center_radius"
    bl_description = ("Add a circle with given center and radius. "
                      "Select a point for the center")
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
      
    
   
    circle_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of sphere",
        soft_min=0.01,
        soft_max=200,
        default=5,
        options={'HIDDEN'},
    )

    
    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) == 1 and
            context.object is not None):
            A = context.active_object
            if (isinstance(A.data, bpy.types.Curve)):
                return False
            else:
                return True
        else: 
            return False   

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.circle_radius = context.scene.geoblender_settings.circle_radius
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
         
               
        circle = new_circle()
        circle_from_center_radius(circle, A, self.circle_radius)
        add_abs_bevel(circle, self.bevel_depth)

        return {'FINISHED'}
