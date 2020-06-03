import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.lines import reflect_across_point




class ReflectionPoint(bpy.types.Operator):
    bl_label = "Reflection about point"
    bl_idname = "geometry.reflection_point"
    bl_description = ("Returns the reflection of a point relative to another"
                      " point (origin of reflection). Select two points. The "
                      " point to be reflected should be the active object")
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
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]
        

        reflect_point = new_point(use_spheres=self.use_spheres,
                                    radius=self.sphere_radius)
        reflect_across_point(reflect_point, A, B)

        return {'FINISHED'}