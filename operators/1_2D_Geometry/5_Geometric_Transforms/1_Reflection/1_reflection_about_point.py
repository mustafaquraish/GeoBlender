import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.utils.objects import duplicate, new_empty
from GeoBlender.geometry.lines import reflect_across_point
from GeoBlender.utils.constraints import locked_track, copy_location
from GeoBlender.utils.constraints import copy_rotation

class ReflectionPoint(bpy.types.Operator):
    bl_label = "Reflection about point"
    bl_idname = "geometry.reflection_point"
    bl_description = ("Returns the reflection of an object relative to a "
                      "point (origin of reflection). Select an object and "
                      "a point. The object should be active")
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
       return (len(context.selected_objects) == 2 
               and context.object is not None
               and context.object in context.selected_objects)

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

            
        C = duplicate(A)
        C.name = "Reflection"
        for constraint in C.constraints:
            C.constraints.remove(constraint) 
        reflect_across_point(C, A, B)
            
        
        e_help_X = new_empty(hide=True)
        e_help_X.parent = A
        e_help_X.location[0] = 1
        e_rot_X = new_empty(hide=True)
        reflect_across_point(e_rot_X, e_help_X, B)

        locked_track(C, 'Z', 'X', e_rot_X)


        return {'FINISHED'}
