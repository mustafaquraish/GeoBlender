import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.intersections import line_line_inteserction




class LineLineInter(bpy.types.Operator):
    bl_label = "Line - Line"
    bl_idname = "geometry.line_line"
    bl_description = ("Returns the intersection of two lines. Select two lines")
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
        
        if not (len(context.selected_objects) == 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve)):
            return False

        if not (isinstance(B.data, bpy.types.Curve)):
            return False

        if 'Line' not in A.data.name:
            return False

        if 'Line' not in B.data.name:
            return False

        return True
        

    def invoke(self, context, event):
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]
        inter = new_point(use_spheres=self.use_spheres,
                           radius=self.sphere_radius)

        line_line_inteserction(inter, A, B, hide_extra=self.hide_extra)  

        




        return {'FINISHED'}