import bpy
import math
from GeoBlender.utils.objects import new_arc, new_empty, duplicate
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver_distance
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.lines import bisecting_line_of_points
from GeoBlender.geometry.lines import bisecting_line_of_line
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, copy_scale

class Scratch(bpy.types.Operator):
    bl_label = "Scratch rOTATION"
    bl_idname = "geometry.create_angle_scratch_rot"
    bl_description = ("Origin is active. Rotate "
                    "Select as many as you want and rotate them")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    

    other_angle: bpy.props.BoolProperty(
        name="Use other side:",
        description="Display the outer angle",
        default=True,
    )

    

    angle_rot: bpy.props.FloatProperty(
        name="Angle of rotation:",
        description="Sets the angle of rotation in degrees",
        min=0,
        soft_max=360,
        default=0.0,
    )
    

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)



    def execute(self, context):
        A = context.active_object
        others = context.selected_objects
        others.remove(A)
        B = others[0]

        #hide=self.hide_extra

        e_rot = new_empty()
        e_rot.name = "e_rot"
        e_loc = new_empty()
        e_loc.name = "e_loc"
        e_center_X_track = new_empty()
        e_center_X_track.name = "e_center_track"
        e_center_X_rotated = new_empty()
        e_center_X_rotated.name = "e_center_rotated"

        e_rot.parent = A
        e_rot.rotation_euler[2] = math.radians(self.angle_rot)

        copy_location(e_center_X_track, B)
        copy_rotation(e_center_X_track, B)
        locked_track(e_center_X_track, 'Z', 'X', A)

        e_center_X_rotated.parent = e_center_X_track
        e_center_X_rotated.rotation_euler[2] = math.radians(self.angle_rot)

        e_loc.parent = e_center_X_rotated

        add_driver_distance(e_loc, 'location', 'X', A, B)
        copy_rotation(e_loc, e_rot) 

        dupli_A = duplicate(A)
        copy_location(dupli_A, e_loc)
        copy_rotation(dupli_A, e_loc)
        copy_scale(dupli_A, A)



        return {'FINISHED'}






        '''
        CODE BELOW!!!


        for x in others:
            rotate(x, A, self.angle_rot)




        

            STEPS:
            1. put an empty at A, copy lr. Call it Rotated objects
            2. dublicate each x. call it dubli_x
            3. put the origin of dubli_x at empty
            4. rotate dubli_x around its Z axis by self.angle_rot degrees

            other approach:
            1. put an empty at A, copy loc, rot of A
            2. add another empty_child and parent it without inverse with empty
            2. copy loc, rot to empty_child of x
            3. rotate the parent empty around its own Z axis (maybe more parent here!) 
               the desired angle. this will rotate the empty_child as we want
            4. copy loc, rot dubli_x from empty_child

            other approach:
            FOR EACH x:
            1. put an empty1 at A, copy loc, rot, lock_track (lock z, x towards x)
            2. dublicate x = dubli_x
            3. take an empty2 and parent it without event to empty1
            4. parent (with inverse!) dubli_x at empty2
            5. rotate empty2 around Z the given number (allow negative values)
            6. the above 5 steps will: rotate dubli_x around A and will be dynamic!

            problem: does not preserve distances yet so no dynamic! 
            we need to DRIVE the distance! also if we dynamically change the orientation
            of x it does not fix the orientation of dubli_x

            It however works if we do it in 2D only for points, lines, circles! just 
            doing the obvious construction.

            maybe there is another idea which combines everything and works for all objects
            in 2d rotation.

            We need two different things. 1) we need to the location of (the centre) of the rotation
            2) we need the orientation of the x-axis of the rotation

            location we can get as above (plus a driver)




        
        
        



            '''