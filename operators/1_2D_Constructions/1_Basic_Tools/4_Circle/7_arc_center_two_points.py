import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver, add_driver_distance
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track



class AngleArcTwoPoints(bpy.types.Operator):
    bl_label = "Arc with center and two endpoints"
    bl_idname = "geometry.create_angle_arc"
    bl_description = ("Arc with given center and the two points. The"
                     " center should be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    '''
    hide: bpy.props.BoolProperty(
        name="Hide:",
        description="hide",
        default=True,
    )
    '''

    other_angle: bpy.props.BoolProperty(
        name="Display the outer angle:",
        description="Display the outer angle",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of arc bevel",
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
     

        arc = new_arc(angle=360, sides=64)

        add_driver_distance(
            obj=arc,
            prop= 'scale',
            fields= 'XYZ', 
            A=A, 
            B=B, 
            scale=1
            )


        
        add_abs_bevel(arc, self.bevel_depth)
        align_to_plane_of(arc, A, B, C)

        if self.other_angle:
            B, C = C, B

        add_driver(
            obj=arc.data,
            prop='bevel_factor_start',
            vars_def={
                'ax': ('transform', A, 'location', 'X'),
                'ay': ('transform', A, 'location', 'Y'),
                'az': ('transform', A, 'location', 'Z'),
                'bx': ('transform', B, 'location', 'X'),
                'by': ('transform', B, 'location', 'Y'),
                'bz': ('transform', B, 'location', 'Z'),
                'cx': ('transform', C, 'location', 'X'),
                'cy': ('transform', C, 'location', 'Y'),
                'cz': ('transform', C, 'location', 'Z'),
            },
            expr='gb_drive_angle_bevel(True,ax,ay,az,bx,by,bz,cx,cy,cz)'
        )

        add_driver(
            obj=arc.data,
            prop='bevel_factor_end',
            vars_def={
                'ax': ('transform', A, 'location', 'X'),
                'ay': ('transform', A, 'location', 'Y'),
                'az': ('transform', A, 'location', 'Z'),
                'bx': ('transform', B, 'location', 'X'),
                'by': ('transform', B, 'location', 'Y'),
                'bz': ('transform', B, 'location', 'Z'),
                'cx': ('transform', C, 'location', 'X'),
                'cy': ('transform', C, 'location', 'Y'),
                'cz': ('transform', C, 'location', 'Z'),
            },
            expr='gb_drive_angle_bevel(False,ax,ay,az,bx,by,bz,cx,cy,cz)'
        )

        return {'FINISHED'}
