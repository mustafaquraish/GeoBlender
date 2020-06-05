import bpy
import mathutils
import math
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.utils.objects import new_arc, new_line
from GeoBlender.geometry.circles import circle_from_center_radius
from GeoBlender.geometry.lines import line_ends, ray
from GeoBlender.utils.drivers import add_driver
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, position_on_curve


class ArcCenter(bpy.types.Operator):
    bl_label = "Translate angle"
    bl_idname = "geometry.translate_angle"
    bl_description = ("Translates an angle with given "
                      "center (active) and a point on one side of the angle "
                      "and equal to another angle (needs existing angle to"
                      " have an arc). Select two points"
                      " and an arc. The center of the angle should "
                      "be the active object" )
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    other_angle: bpy.props.BoolProperty(
        name="Display the outer angle:",
        description="Display angle at the opposite side",
        default=True,
    )

    hide_arc: bpy.props.BoolProperty(
        name="Hide arc:",
        description="Hide the arc",
        default=False,
    )

    hide_endpoints: bpy.props.BoolProperty(
        name="Hide endpoints:",
        description="Hide the arc endpoints",
        default=True,
    )

    display_sides: bpy.props.BoolProperty(
        name="Display sides:",
        description="Display the angle sides",
        default=False,
    )

    arc_angle: bpy.props.FloatProperty(
        name="Angle:",
        description="Angle of arc",
        min=0,
        soft_max=360,
        default=90,
    )

    radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of arc",
        min=0.01,
        soft_max=20,
        default=1,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of arc",
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
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        (B, arc_old) = others
        
        '''
        idea is the following
        form arc_old determine:
        1. center copy_location:A_old
        2. end1_old:B_old NOW WAY TO GET THESE WITHOUT ACCESSING THE BEVEL! 
        SO WE NEED TO DRIVE FROM THE BEVEL!
        3. end2_old:C_old
        that gives the angle BAC
        we can then reverse the whole process
        put arc_new as in mustafa's construction
        the only thing is that we do not have the Y point here
        so we need to take the one orientation
        we can copy_rotation of arc_old and so we immediately get the reversal
        so then we only need to drive the same bevel function
        now if we want the other side what do we do?
        we need to flip the orientation of the arc? how, using 
        constraints and an object on the Y axis and locking X and then trakcing -Y.
        
        and the drive using the x,y,z coordinates of the points a,b,c_old

        '''
        arc_neo = new_arc(angle=360, sides=64)
        copy_location(arc_neo, A)
        copy_rotation(arc_neo, A)
        locked_track(arc_neo, 'Z', 'X', B)

        for i in range(3):
            arc_neo.scale[i] = self.radius
        add_abs_bevel(arc_neo, self.bevel_depth)
        
        if self.other_angle:
            arc_neo.data.bevel_factor_start = 0
            arc_neo.data.bevel_factor_end = self.arc_angle / 360
            end1 = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius,
                            hide=self.hide_endpoints)
            end1.name = "Arc endpoint"
            end2 = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius,
                            hide=self.hide_endpoints)
            end2.name = "Arc endpoint"
            position_on_curve(end1, arc_neo, position=0)
            position_on_curve(end2, arc_neo, position=self.arc_angle / 360)   
            if self.display_sides:
                side1 = new_line()
                add_abs_bevel(side1, self.bevel_depth)
                side2 = new_line()
                add_abs_bevel(side2, self.bevel_depth)
                ray(side1, A, end1)
                ray(side2, A, end2)

        else:
            arc_neo.data.bevel_factor_start = self.arc_angle / 360
            arc_neo.data.bevel_factor_end = 1
            end1 = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius,
                            hide=self.hide_endpoints)
            end1.name = "Arc endpoint"
            end2 = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius,
                            hide=self.hide_endpoints)
            end2.name = "Arc endpoint"
            position_on_curve(end1, arc_neo, position=self.arc_angle / 360)
            position_on_curve(end2, arc_neo, position=1) 
            if self.display_sides:
                side1 = new_line()
                add_abs_bevel(side1, self.bevel_depth)
                side2 = new_line()
                add_abs_bevel(side2, self.bevel_depth)
                ray(side1, A, end1)
                ray(side2, A, end2)   

        


        return {'FINISHED'}
