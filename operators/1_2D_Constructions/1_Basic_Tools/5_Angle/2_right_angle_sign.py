import bpy
import mathutils
import math
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.utils.objects import new_arc, new_right_angle, new_empty
from GeoBlender.utils.objects import set_parent
from GeoBlender.geometry.circles import circle_from_center_radius
from GeoBlender.utils.drivers import add_driver
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, damped_track
from GeoBlender.utils.geometry import align_to_plane_of





class RightAngle(bpy.types.Operator):
    bl_label = "Right angle"
    bl_idname = "geometry.right_angle"
    bl_description = ("Add a right angle with given  center and one point"
                      " on each of the two sides of the angle."
                      " Select three points. The center should "
                      "be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

 
 


    

    

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of right angle",
        min=0.01,
        soft_max=20,
        default=1,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of angle",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    

  

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        B, C = others

        arc_neo = new_right_angle(length=self.length)
        add_abs_bevel(arc_neo, self.bevel_depth)

        center = new_empty() #hide=self.hide_extra
        copy_location(center, A)
        damped_track(center, axis='-X', target=B)
        locked_track(center, axis='-Y', lock='X', target=C)

        #set_parent(arc_neo, center)
        arc_neo.parent = center
        arc_neo.location[0] = - self.length 
        arc_neo.location[1] = - self.length 



             
        



        return {'FINISHED'}