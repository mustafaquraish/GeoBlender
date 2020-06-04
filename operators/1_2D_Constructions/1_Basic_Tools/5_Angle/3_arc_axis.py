import bpy
import mathutils
import math
from GeoBlender.utils.objects import new_point, new_circle, add_abs_bevel
from GeoBlender.utils.objects import new_arc
from GeoBlender.geometry.circles import circle_from_center_radius
from GeoBlender.utils.drivers import add_driver
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track


class ArcCenter(bpy.types.Operator):
    bl_label = "Arc with axis"
    bl_idname = "geometry.arc_center_angle"
    bl_description = ("Add the arc of an angle with given axis."
                      " The axis is determined by the center of "
                      " the arc and another point one side of the angle. "
                      "Select two points. The center should "
                      "be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    other_angle: bpy.props.BoolProperty(
        name="Display the outer angle:",
        description="Display the outer angle",
        default=True,
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
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        arc_neo = new_arc(angle=360, sides=64)
        copy_location(arc_neo, A)
        copy_rotation(arc_neo, A)
        locked_track(arc_neo, 'Z', 'X', B)

        for i in range(3):
            arc_neo.scale[i] = self.radius
        arc_neo.data.bevel_depth = self.bevel_depth / self.radius
        if self.other_angle:
            arc_neo.data.bevel_factor_start = 0
            arc_neo.data.bevel_factor_end = self.arc_angle / 360
        else:
            arc_neo.data.bevel_factor_start = self.arc_angle / 360
            arc_neo.data.bevel_factor_end = 1

        return {'FINISHED'}
