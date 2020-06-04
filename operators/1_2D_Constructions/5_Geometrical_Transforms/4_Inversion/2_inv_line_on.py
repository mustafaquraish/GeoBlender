import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.inversions import inversion_on_line




class InversionLineOn(bpy.types.Operator):
    bl_label = "Inversion of line (on)"
    bl_idname = "geometry.inversion_line"
    bl_description = ("Adds the inversion of a line in the case where the"
                      " line goes through the origin of inversion."
                      " Select the line (active) and a circle."
                      " The center of the circle is the origin and the "
                      " square of the radius is the power of inversion") 
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
      

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
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
        if (len(context.selected_objects) == 2  and
                context.object is not None):
            A = context.active_object
            others = context.selected_objects[-2:]
            others.remove(A)
            B = others[0]

            if not (isinstance(B.data, bpy.types.Curve) and 
                        (isinstance(A.data, bpy.types.Curve))):
                return False

            if 'Circle' not in B.data.name:
                return False

            if 'Line' not in A.data.name:
                return False

            else:
                return True

        else:
            return False

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]
        

        inv_line = new_line(length=self.length)
        add_abs_bevel(inv_line, self.bevel_depth)
        inversion_on_line(inv_line, A, B)

        return {'FINISHED'}