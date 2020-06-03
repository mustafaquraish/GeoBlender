import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.lines import bisecting_line_of_points
from GeoBlender.geometry.lines import bisecting_line_of_line





class PerpBisector(bpy.types.Operator):
    bl_label = "Perpendicular bisector"
    bl_idname = "geometry.perp_bisector"
    bl_description = ("Returns the line the perpendicular bisector of"
                      " a line. Select either two points"
                      " or a line")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
      
    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
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
        
        if (len(context.selected_objects) == 2):
            return True

        if (len(context.selected_objects) == 1):

            A = context.active_object
            
            
            if not (isinstance(A.data, bpy.types.Curve)):
                return False

            elif 'Line' not in A.data.name:
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

        if  (len(context.selected_objects) == 2): 
            (B, C) = context.selected_objects[-2:]
            
                   
        
            obj = new_line(length=self.length)
            add_abs_bevel(obj, self.bevel_depth)


            bisecting_line_of_points(obj, B, C, hide_extra=self.hide_extra)
                  
        

        if  (len(context.selected_objects) == 1):
            A = context.active_object
            obj = new_line(length=self.length)
            add_abs_bevel(obj, self.bevel_depth)


            bisecting_line_of_line(obj, A, hide_extra=self.hide_extra)


        
        return {'FINISHED'}