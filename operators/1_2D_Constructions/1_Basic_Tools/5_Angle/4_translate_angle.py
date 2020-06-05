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
    bl_description = ("Adds an angle with given "
                      "center (active) and a point on one side of the angle "
                      "and equal to another angle (needs existing angle to"
                      " have an arc). Select two points"
                      " and an arc. The center of the new angle should "
                      "be the active object" )
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    other_side: bpy.props.BoolProperty(
        name="Opposite orientation:",
        description="Display angle at the opposite side",
        default=False,
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

   
    

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of arc",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    radius: bpy.props.FloatProperty(
        name="Arc radius:",
        description="Radius of arc",
        min=0.01,
        soft_max=20,
        default=1,
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Point radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
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
        (B_test, arc_old_test) = others

        if 'Arc' in B_test.data.name:
            arc_old = B_test
            B = arc_old_test
        if 'Arc' in arc_old_test.data.name:
            arc_old = arc_old_test
            B = B_test
        
       
        empty1 = new_point(hide=True)
        empty1.parent = arc_old
        empty1.location[1] = -1

        fl_arc_old = new_point(hide=True)
        copy_location(fl_arc_old, arc_old)
        locked_track(fl_arc_old,'X', 'Y', empty1)

        arc_neo = new_arc(angle=360, sides=64, hide=self.hide_arc)
        for i in range(3):
            arc_neo.scale[i] = self.radius
        add_abs_bevel(arc_neo, self.bevel_depth)
        copy_location(arc_neo, A)

        if self.other_side:
            copy_rotation(arc_neo, fl_arc_old)
        else:
            copy_rotation(arc_neo, arc_old)

        locked_track(arc_neo, 'Z', 'X', B)
        

        add_driver(
                obj=arc_neo.data,
                prop= 'bevel_factor_start',
                vars_def={
                    'bev': ('datapath', arc_old, 'data.bevel_factor_start'),},
                expr= 'bev'
                )  

        
        add_driver(
                obj=arc_neo.data,
                prop= 'bevel_factor_end',
                vars_def={
                    'bev': ('datapath', arc_old, 'data.bevel_factor_end'),},
                expr='bev'
                )  

        end1 = new_point(radius=self.sphere_radius, hide=self.hide_endpoints)
        end1.name = "Arc endpoint"
        end2 = new_point(radius=self.sphere_radius, hide=self.hide_endpoints)
        end2.name = "Arc endpoint"
        position_on_curve(end1, arc_neo, position=0)
        position_on_curve(end2, arc_neo, position=1) 

        add_driver(
                obj=end1.constraints[-1],
                prop= 'offset_factor',
                vars_def={
                    'bev': ("datapath", arc_neo, "data.bevel_factor_start"),},
                expr= "bev"
                )

        add_driver(
                obj=end2.constraints[-1],
                prop= 'offset_factor',
                vars_def={
                    'bev': ("datapath", arc_neo, "data.bevel_factor_end"),},
                expr= "bev"
                ) 

        if self.display_sides:
                side1 = new_line()
                add_abs_bevel(side1, self.bevel_depth)
                side2 = new_line()
                add_abs_bevel(side2, self.bevel_depth)
                ray(side1, A, end1)
                ray(side2, A, end2)  






        return {'FINISHED'}
