import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.utils.objects import new_empty, duplicate
from GeoBlender.geometry.lines import reflect_across_line
from GeoBlender.geometry.lines import reflect_across_line_of_points
from GeoBlender.utils.constraints import copy_rotation, copy_location
from GeoBlender.utils.constraints import locked_track

class MidpointRef(bpy.types.Operator):
    bl_label = "Reflection about a line"
    bl_idname = "geometry.reflection_line"
    bl_description = ("Returns the reflection of an object relative to a"
                      " line (line of reflection). Select an object and "
                      "a line. The object should be active")
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

        if (len(context.selected_objects) == 2 and
                context.object is not None):
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

        if (len(context.selected_objects) == 2 and
                context.object is not None):
            A = context.active_object
            others = context.selected_objects[-2:]
            others.remove(A)
            B = others[0]

            
            C = duplicate(A)
            C.name = "Reflection"
            for constraint in C.constraints:
               C.constraints.remove(constraint) 
            reflect_across_line(C, A, B)
            
        
            e_help_X = new_empty(hide=True)
            e_help_X.parent = A
            e_help_X.location[0] = 1
            e_rot_X = new_empty(hide=True)
            reflect_across_line(e_rot_X, e_help_X, B)

            locked_track(C, 'Z', 'X', e_rot_X)











        

            

        return {'FINISHED'}
